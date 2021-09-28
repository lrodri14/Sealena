"""
    This views.py contains all the synchronous functions and asynchronous functions needed or required for the Appointments,
    there is also a new loop created to run the asynchronous functions, it is stored inside 'loop' variable, this file
    is composed of two async functions and fourteen synchronous functions, twelve of them views.
"""

# Imports
import asyncio
from datetime import datetime
from django.db.models import Q
from Sealena import settings
from django.utils import timezone
from django.shortcuts import render
from django.http import JsonResponse
from django.db import IntegrityError
from django.shortcuts import redirect
from patients.models import Patient
from .models import BaseConsult, MedicalTestResult, VaccineApplication, Surgery
from utilities.accounts_utilities import speciality_mapping
from django.template.loader import render_to_string
from .forms import DrugForm, DrugCategoryFilterForm, MedicalTestForm, MedicalTestTypeFilterForm, \
    MedicalTestResultFormset, AgendaDateFilterForm, RegisterFilterForm, VaccineCreationAndUpdateForm, \
    SurgeryCreationAndUpdateForm, VaccineApplicationCreationAndUpdateForm, SurgicalConsultCreationForm, \
    ConsultDetailsFilterForm
from utilities.appointments_utilities import evaluate_consult, generate_pdf, send_sms, check_delayed_consults, \
                                            collect_months_names, filter_conditional_results

# Import is unused because we will use it in a future update.
from .tasks import save_new_drug

# New Event Loop
loop = asyncio.new_event_loop()

# Create your views here.


def appointments(request):
    """
        DOCSTRING:
        This appointments() view is used to render the main appointments page, in here the user will be able to see the
        appointments that are pending for the current date and also the consults that were locked for further changes, it will retrieve the
        appointments using a filter, also this view will check if the user who requested this page belongs to the Doctor's
        group, this for editing logic that will be managed in the template. Since the results will be paginated, we need to
        check if the 'page' parameter exists in our 'GET' dictionary, depending of the value of the parameter, the
        function will decide which page should it return, if the 'page' parameters, doesn't exists, the context will be
        rendered, if not, then the context will be rendered and returned as string, so we can send it in a JSON Format.
        It expects only one argument, 'request', it waits for an object request, This view will render the content if
        the page is not a valid number, if it is, the response will be returned in JSON Format.

        # Subscription Logic #

        When users navigate making use of a Basic Account, they are limited to 10 records, a message will be displayed
        with information about the still available records.

        *Note: the collection of appointments from user with Assistant roll, is based on the indexing syntax, since assistants
         can only be linked to a single doctor, this before we build up the multiple linking functionality in future updates.*

    """
    today = timezone.localtime().date()
    if request.user.roll == 'DOCTOR':
        aimed_user = request.user
    else:
        aimed_user = request.user.assistant.doctors.all()[0]

    message = None
    records_left = 10 - len(BaseConsult.objects.filter(created_by=aimed_user)[:10])
    subscription = aimed_user.doctor.subscription
    if subscription == 'BASIC':
        if request.user.roll == 'DOCTOR':
            message = 'You are using a Sealena Basic account, you have {} records left'.format(records_left)
        else:
            message = 'The user you are linked to has Sealena Basic account, it has {} records left'.format(records_left)

    appointments_list = BaseConsult.objects.filter(Q(created_by=aimed_user, datetime__date=today, medical_status=False, status='CONFIRMED') | Q(created_by=aimed_user, lock=False)).order_by('datetime')
    template = 'appointments/appointments.html'
    context = {'appointments': appointments_list, 'message': message}
    return render(request, template, context)


def create_appointment(request, pk=None):
    """
        DOCSTRING:

        This create_appointment function view is used to create consult appointments, based on the doctor's speciality,
        a specific creation form will be used to create a consult instance (called appointment at this point). We'll
        retrieve that specific creation form making use of our speciality_mapping dictionary inside our accounts utilities.
        We'll pass the request.user to the class, this because we need to manage some logic inside this class, such as
        the displaying of patients only related to the current user, the only thing inside our view context is this form,
        we will return the data in JSON Format, so the rendering we convert it into a string with the use of the
        render_to_string() function, and send the data as a JSONResponse. If the request.method is  a 'POST', then we
        populate the form with the content inside the request.POST dictionary, and we check if the form is valid, if it is,
        then the consult will be saved and added to the agenda so we can then confirm it, edit it or cancel it, if the form
        is not valid, then we will add a custom error to the context and render the template again so we can send it back
        as a JSONResponse. This view only expects an argument, 'request', should be a request object.

        # Subscription Logic #

        When users navigate making use of a Basic Account, they are limited to 10 records, whenever they reach their limit
        a message will be displayed instead of the form. A different message will be displayed to the Doctor type accounts
        and the Assistant type accounts.

        * Note: the collection of patients from user with Assistant roll, is based on the indexing syntax, since assistants
         can only be linked to a single doctor, this before we build up the multiple linking functionality in future updates. *

    """
    if request.user.roll == 'DOCTOR':
        aimed_user = request.user
    else:
        aimed_user = request.user.assistant.doctors.all()[0]

    creation_form = speciality_mapping[aimed_user.doctor.speciality]['creation_form']
    consults_form = creation_form(user=aimed_user)

    # Variable used to display the patient addition button if necessary
    addition_button = True

    if pk is not None:
        patient = Patient.objects.get(pk=pk)
        consults_form.initial = {'patient': patient}
        addition_button = False

    template = 'appointments/create_appointment.html'
    context = {'addition_button': addition_button}
    data = {}

    if request.method == 'POST':
        consults_form = creation_form(request.POST, user=aimed_user)
        if consults_form.is_valid():
            try:
                consult = consults_form.save(commit=False)
                consult.created_by = aimed_user
                consult.save()
                if aimed_user.doctor.subscription == 'PREMIUM':
                    loop.run_until_complete(send_sms(consult))
                data['success'] = 'Consult created successfully'
                data['datetime'] = consult.datetime.strftime('%B %-d, %Y at %I:%M %p')
                data['created_by'] = request.user.username if request.user.roll == 'ASSISTANT' else 'You'
                data['to'] = request.user.username if request.user.roll == 'DOCTOR' else request.user.assistant.doctors.all()[0].username
                if 'patients' in request.META['HTTP_REFERER']:
                    consults = BaseConsult.objects.filter(patient=consult.patient)
                    context['consults_filter_form'] = ConsultDetailsFilterForm
                    template = 'patients/patient_consults_list.html'
                    context['consults'] = consults
            except IntegrityError:
                date = consults_form.cleaned_data.get('datetime').date()
                time = consults_form.cleaned_data.get('datetime').time().strftime('%I:%M:%S %p')
                context['error'] = 'There is already a reservation for {} at {}'.format(date, time)

    message = None
    creation_enabled = True
    records_left = 10 - len(BaseConsult.objects.filter(created_by=aimed_user)[:10])
    account_type = aimed_user.doctor.subscription
    if account_type == 'BASIC':
        if request.user.roll == 'DOCTOR':
            message = 'You are currently using a Sealena Basic account, you have {} ' \
                      'records left, if you want to continue creating appointments ' \
                      'please switch your account to Premium by following this path ' \
                      '(Settings > Account > Go Premium)'.format(records_left)
        else:
            message = 'The user you are linked to uses a Sealena Basic account, it has {} ' \
                      'records left, to continue creating appointments the account must be' \
                      'switched from Basic to Premium '.format(records_left)

        if records_left <= 0:
            creation_enabled = False

    context['consults_form'] = consults_form
    context['message'] = message
    context['creation_enabled'] = creation_enabled
    data['html'] = render_to_string(template, context, request)
    return JsonResponse(data)


def consults_details(request, pk):
    """
        DOCSTRING:
        This consult_details() view is used to display the details of a single consult, as well as the exams related to
        that consult in case there are, this view will also check for the HTTP_REFERER headers, this so it can know where
        to redirect if the user wants to go to the page it was before. There are some things we need to collect before
        displaying the consult details, and that is the consult model used by the doctor's speciality to create appointments
        and consults. We'll make use of the speciality_mapping dictionary utility inside our accounts utilities.
        It takes two arguments, 'request' which expects a request object, and 'pk', which expects the pk of a specific consult.
    """
    consult_model = speciality_mapping[request.user.doctor.speciality]['model']
    consult = consult_model.objects.get(pk=pk)
    exams = MedicalTestResult.objects.filter(consult=consult) if len(MedicalTestResult.objects.filter(consult=consult)) > 0 else None
    template = 'appointments/consult_details.html'
    context = {'consult': consult, 'exams': exams}
    if 'patients/details' in request.META.get('HTTP_REFERER'):
        context['referer'] = 'details'
    else:
        context['referer'] = 'appointments'
    return render(request, template, context)


def consult_summary(request, pk):
    """
        DOCSTRING:
        This consult_summary() view is used to display the summary of a single consults, it will only display the motive
        and suffering of the patient, which is why he attended that day, if there were any diagnose or treatments, they
        will displayed as well, the result of this view will be displayed inside the consults update template, so the
        response must be sent in JSON Format, we use the render_to_string function to convert it into a string and we
        send the response as a JSON Response. It takes two arguments, 'request' which expects a request object, and
        'pk', which expects the pk of a specific consult.
    """
    consult = BaseConsult.objects.get(pk=pk)
    template = 'appointments/consult_summary.html'
    context = {'consult': consult}
    data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)


def update_consult(request, pk):
    """
        DOCSTRING:
        This update_consult() function view is used to fill up appointments that were created through the create_consult()
        function view. The form used to fill the consult contains information of a previously populated consult instance.
        Therefore we need to collect the model used by the Doctor to create consults. We'll make use of the speciality_mapping
        dictionary utility to retrieve the model.

        Besides the main consult form, we use three extra forms to attach extra information to the actual consult.
        'MedicalExamsFormset' used to create as many exams instances for this consult as needed, 'DrugsForm' used to create
        drugs asynchronously and 'DrugCategoryFilterForm' used to filter drugs inside the consult.

        If the request.method is a 'GET' method, then it will render the template with these 4 forms and display it to
        the user in the response. If the request.method is 'POST' then 'UpdateConsultForm' and the 'MedicalExamsFormset'
        will be populated with the request.POST dictionary content and check if both of them is valid, they won't be saved
        and commited yet, there are a few things we need to check before.

        For each exam in the medical exams formset, we need to check if there are any forms with the DELETE attribute set to True,
        each of them which contains the check will be deleted and not saved and set the consult attribute to the current consult,
        the rest will be commited, for the consult we will set it's medical_status attribute to True, when this is done we will
        save the many to many relationship with the drugs if needed. If there was an error with the medical exams, then a custom error
        will be added to the context and the template will be rendered again.

        It takes two arguments, 'request' which expects a request object and 'pk' which expects a consult's pk finally,
        the evaluate_consult function will be called to inspect if any important indications or prescriptions for the
        patient where made in order to handle the user a receipt for the patient, if this function returns True,
        then the create_pdf function will be called and the prescription will be created, afterwards the prescription's
        path will be sent to the user in JsonFormat.
    """
    consult_model = speciality_mapping[request.user.doctor.speciality]['model']
    consult = consult_model.objects.get(pk=pk)
    updating_form = speciality_mapping[request.user.doctor.speciality]['updating_form']
    consult_form = updating_form(request.POST or None, user=request.user, instance=consult)
    medical_test_result_formset = MedicalTestResultFormset()
    drug_form = DrugForm
    drug_category_filter_form = DrugCategoryFilterForm
    medical_test_form = MedicalTestForm
    medical_test_filter_form = MedicalTestTypeFilterForm
    template = 'appointments/update_consult.html'
    context = {'consult': consult, 'consult_form': consult_form, 'medical_test_result_formset': medical_test_result_formset,
               'drug_form': drug_form, 'drug_category_filter_form': drug_category_filter_form, 'medical_test_form': medical_test_form,
               'medical_test_filter_form': medical_test_filter_form}

    if request.method == 'POST':
        consult_form = updating_form(request.POST or None, user=request.user, instance=consult)
        medical_test_result_formset = MedicalTestResultFormset(request.POST, request.FILES)
        if consult_form.is_valid() and medical_test_result_formset.is_valid():
            consult = consult_form.save(commit=False)
            medical_test_instances = medical_test_result_formset.save(commit=False)

            consult.medical_status = True
            consult.save()
            consult_form.save_m2m()

            for medical_test_instance in medical_test_instances:
                medical_test_instance.consult = consult
                medical_test_instance.save()

            # Consult Evaluation
            if evaluate_consult(consult):
                generate_pdf('appointments/consult_pdf.html', consult, request.user)
                return JsonResponse({'prescription_path': settings.MEDIA_URL + consult.prescription.name})

            return redirect('appointments:appointments')

        elif not medical_test_result_formset.is_valid():
            context['error'] = '* Exams not filled correctly. "Type" & "Image" fields must be provided.'

    return render(request, template, context)


def add_vaccination_record(request, pk):
    """
        DOCSTRING: This add_vaccination_record view, expects a request as it's unique parameter, this view will return
        two different response based on the HTTP request method, if the method is GET then it will return the form used
        to create VaccineApplication instances, if the request is a POST request and the form it's valid, it will return
        a success response.
    """

    patient = Patient.objects.get(pk=pk)
    form = VaccineApplicationCreationAndUpdateForm(user=request.user)
    template = 'appointments/add_vaccination_record.html'

    if request.method == 'POST':
        form = VaccineApplicationCreationAndUpdateForm(request.POST, user=request.user)
        if form.is_valid():
            vaccination_record = form.save(commit=False)
            vaccination_record.patient = patient
            vaccination_record.save()
            updated_vaccination_records = VaccineApplication.objects.filter(patient=patient)
            template = 'patients/patient_vaccines_list.html'
            context = {'vaccines': updated_vaccination_records, 'consults_filter_form': ConsultDetailsFilterForm, 'patient': patient}
            data = {'html': render_to_string(template, context, request)}
            return JsonResponse(data)

    context = {'form': form, 'patient': patient}
    data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)


def update_vaccination_record(request, record_pk, patient_pk):
    """
        DOCSTRING: This update_vaccination_record view, expects a request and pk as parameters, this view will return
        two different response based on the HTTP request method, if the method is GET then it will return the form used
        to update VaccineApplication instances, if the request is a POST request and the form it's valid, it will return
        a success response.
    """
    vaccination_record = VaccineApplication.objects.get(pk=record_pk)
    patient = Patient.objects.get(pk=patient_pk)
    form = VaccineApplicationCreationAndUpdateForm(instance=vaccination_record, user=request.user)

    if request.method == 'POST':
        form = VaccineApplicationCreationAndUpdateForm(request.POST, instance=vaccination_record, user=request.user)

        if form.is_valid():
            updated_record = form.save(commit=False)
            updated_record.patient = patient
            updated_record.save()
            template = 'patients/patient_vaccines_list.html'
            updated_vaccination_records = VaccineApplication.objects.filter(patient=patient)
            context = {'vaccines': updated_vaccination_records, 'consults_filter_form': ConsultDetailsFilterForm, 'patient': patient}
            data = {'html': render_to_string(template, context, request)}
            return JsonResponse(data)

    template = 'appointments/update_vaccination_record.html'
    context = {'form': form, 'record': vaccination_record, 'patient': patient}
    data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)


def vaccination_record_details(request, pk):
    """
        DOCSTRING: This vaccination_record_details receives two parameters, the request and the pk of the instance we are
        trying to visualize, this will return the instance details.
    """
    vaccination_record = VaccineApplication.objects.get(pk=pk)
    template = 'appointments/vaccination_record_details.html'
    context = {'record': vaccination_record}
    data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)


def delete_vaccination_record(request, record_pk, patient_pk):
    """
        DOCSTRING: This delete_vaccination_record view, expects a request and pk as parameters, this view will return
        two different response based on the HTTP request method, if the method is GET then it will return the form used
        to delete VaccineApplication instances, if the request is a POST request it will delete the instance and it will return
        a success response.
    """
    vaccination_record = VaccineApplication.objects.get(pk=record_pk)
    patient = Patient.objects.get(pk=patient_pk)
    if request.method == 'POST':
        vaccination_record.delete()
        update_vaccination_records = VaccineApplication.objects.filter(patient=patient)
        template = 'patients/patient_vaccines_list.html'
        context = {'vaccines': update_vaccination_records, 'consults_filter_form': ConsultDetailsFilterForm, 'patient': patient}
        data = {'html': render_to_string(template, context, request)}
        return JsonResponse(data)
    template = 'appointments/delete_vaccination_record.html'
    context = {'record': vaccination_record, 'patient': patient}
    data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)


# Assisted Surgery - Coming up in updates!

# def appoint_surgery(request, pk):
#     """
#         DOCSTRING: This appoint_surgery view, expects a request as it's unique parameter, this view will return
#         two different response based on the HTTP request method, if the method is GET then it will return the form used
#         to create Surgery instances, if the request is a POST request and the form it's valid, it will return
#         a success response.
#     """
#     patient = Patient.objects.get(pk=pk)
#     form = SurgeryCreationAndUpdateForm
#     if request.method == 'POST':
#         form = SurgeryCreationAndUpdateForm(request.POST)
#         if form.is_valid():
#             surgery = form.save(commit=False)
#             surgery.patient = patient
#             surgery.save()
#             return JsonResponse({'success': True})
#     template = 'appointments/create_surgery_appointment.html'
#     context = {'form': form}
#     data = {'html': render_to_string(template, context, request)}
#     return JsonResponse(data)
#
#
# def update_surgery_record(request, pk):
#     """
#         DOCSTRING: This update_surgery_record view, expects a request and pk as parameters, this view will return
#         two different response based on the HTTP request method, if the method is GET then it will return the form used
#         to update Surgery instances, if the request is a POST request and the form it's valid, it will return
#         a success response.
#     """
#     surgery_appointment = Surgery.objects.get(pk=pk)
#     form = SurgeryCreationAndUpdateForm(instance=surgery_appointment)
#     if request.method == 'POST':
#         form = SurgeryCreationAndUpdateForm(request.POST, instance=surgery_appointment)
#         if form.is_valid():
#             form.save()
#             return JsonResponse({'success': True})
#     template = 'appointments/update_surgery_appointment.html'
#     context = {'form': form}
#     data = {'html': render_to_string(template, context, request)}
#     return JsonResponse(data)
#
#
# def surgery_details(request, pk):
#     """
#         DOCSTRING: This surgery_details receives two parameters, the request and the pk of the instance we are
#         trying to visualize, this will return the instance details.
#     """
#     surgery_appointment = Surgery.objects.get(pk=pk)
#     template = 'appointments/surgery_details.html'
#     context = {'surgery': surgery_appointment}
#     data = {'html': render_to_string(template, context, request)}
#     return JsonResponse(data)
#
#
# def cancel_surgery_appointment(request, pk):
#     """
#         DOCSTRING: This cancel_surgery_appointment view, expects a request and pk as parameters, this view will return
#         two different response based on the HTTP request method, if the method is GET then it will return the form used
#         to cancel Surgery instances, if the request is a POST request it will delete the instance and it will return
#         a success response.
#     """
#     surgery_appointment = Surgery.objects.get(pk=pk)
#     if request.method == 'POST':
#         surgery_appointment.status = 'CANCELLED'
#         return JsonResponse({'success': True})
#     template = 'appointments/cancel_surgery_appointment.html'
#     context = {'surgery': surgery_appointment}
#     data = {'html': render_to_string(template, context, request)}
#     return JsonResponse(data)


def agenda(request):
    """
        DOCSTRING:
        The agenda() view is used to render all the consults that are pending from today's date to the greater date a
        consult was registered, they are also classified by month, this means that no matter if there is only a consult
        scheduled for november, that month will appear in the template, we will also render the AgendaFilterForm, this
        so that we can perform filtering processes with the data we have at our disposal in the agenda, we need to render
        the name of the months our consults are scheduled, for this we store the result returned from our collect_months_names()
        function into a variable called 'months_names', along with the filtering form and the consults,this function will also verify that
        there is a 'page' parameter in the request.GET dict, if there is no parameter, then the first page is shown, else the
        asking page will be shown to the user. This function takes only one argument: 'request' which expects a request object.

        *Note: the collection of agenda appointments from user with Assistant roll, is based on the indexing syntax, since assistants
         can only be linked to a single doctor, this before we build up the multiple linking functionality in future updates.*

    """
    if request.user.roll == 'DOCTOR':
        aimed_user = request.user
    else:
        aimed_user = request.user.assistant.doctors.all()[0]

    today = timezone.localtime().date()
    tzone = timezone.get_current_timezone()
    appointments_list = BaseConsult.objects.filter(created_by=aimed_user, datetime__date__gte=today, medical_status=False).order_by('datetime')
    months_names = collect_months_names(appointments_list, tzone)
    form = AgendaDateFilterForm
    template = 'appointments/agenda.html'
    context = {'appointments': appointments_list, 'months': months_names, 'form': form, 'today': today}
    return render(request, template, context)


def filter_agenda(request):
    """
        This filter_agenda is used to filter the consults belonging to this user, depending on the parameters values inside the
        request.GET dictionary, this function will collect the 'date_from' parameter and 'date_to' parameter values and convert
        them into a datetime object, this way we can filter the consults based on this values, finally we will return our response
        in JSON Format, this function also checks if the 'page' parameter is inside the querystring, if it is, then the page that
        will be rendered will be that one in the 'page' value, else the first page will be rendered.

        *Note: the collection of agenda appointments from user with Assistant roll, is based on the indexing syntax, since assistants
         can only be linked to a single doctor, this before we build up the multiple linking functionality in future updates.*
    """
    if request.user.roll == 'DOCTOR':
        aimed_user = request.user
    else:
        aimed_user = request.user.assistant.doctors.all()[0]

    tzone = timezone.get_current_timezone()
    template = 'appointments/partial_agenda_list.html'
    query_date_from = datetime.strptime(request.GET.get('date_from'), "%Y-%m-%d")
    query_date_to = datetime.strptime(request.GET.get('date_to'), "%Y-%m-%d")
    consults_list = BaseConsult.objects.filter(datetime__date__gte=query_date_from, datetime__date__lte=query_date_to, created_by=aimed_user).order_by('datetime')
    months = collect_months_names(consults_list, tzone)
    context = {'appointments': consults_list, 'months': months}
    data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)


def appointment_date_update(request, pk):
    """
        DOCSTRING:
        This appointment_date_update() view is used to update the date of a specific consult, this view will collect that
        specific consult form the database and the ConsultsForm, since this process will be done asynchronously, we need
        to return our response in JSON Format, for this we use our render_to_string function, if the request.method is
        'GET' we return this response in JSON Format, if the request.method is 'POST' we fill our form with the
        content inside our request.POST dict and check if it is valid or not, if it is not then we will add a custom
        error and return the response again, if it is we save this consult's new date and return in JSON Format the
        updated content, so the registers will be updated asynchronously in the front-end. It takes two arguments,
        'request' which expects a request object and 'pk' which expects a consult.pk key.

        *Note: the collection of appointments from user with Assistant roll, is based on the indexing syntax, since assistants
         can only be linked to a single doctor, this before we build up the multiple linking functionality in future updates.*
    """
    if request.user.roll == 'DOCTOR':
        aimed_user = request.user
    else:
        aimed_user = request.user.assistant.doctors.all()[0]

    today = timezone.localtime().date()
    tzone = timezone.get_current_timezone()
    consult = BaseConsult.objects.get(pk=pk)
    form = AgendaDateFilterForm
    creation_form = speciality_mapping[aimed_user.doctor.speciality]['creation_form']
    consult_form = creation_form(request.POST or None, instance=consult, user=aimed_user)
    template = 'appointments/appointment_date_update.html'
    context = {'consult_form': consult_form, 'consult': consult}
    data = {'html': render_to_string(template, context, request)}
    if request.method == 'POST':
        consult_form = creation_form(request.POST or None, instance=consult, user=aimed_user)
        if consult_form.is_valid():
            try:
                consult_form.save()
                loop.run_until_complete(send_sms(consult))
                consults_list = BaseConsult.objects.filter(created_by=aimed_user, datetime__date__gte=today, medical_status=False).order_by('datetime')
                months_names = collect_months_names(consults_list, tzone)
                data = {'updated_html': render_to_string('appointments/partial_agenda_list.html', {'appointments': consults_list, 'months': months_names, 'form': form}, request=request)}
                data['to'] = request.user.username if request.user.roll == 'DOCTOR' else request.user.assistant.doctors.all()[0].username
                data['patient'] = consult.patient.first_names + ' ' + consult.patient.last_names
                data['datetime'] = consult.datetime.strftime('%B %-d, %Y at %I:%M %p')
            except IntegrityError:
                date = consult_form.cleaned_data.get('datetime').date()
                time = consult_form.cleaned_data.get('datetime').time().strftime('%I:%M:%S %p')
                context['error'] = 'There is already a reservation for {} at {}'.format(date, time)
                data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)


def confirm_appointment(request, pk):
    """
        DOCSTRING:
        This confirm_appointment() view is used to confirm the consult, it will set the consult.status attribute from pending
        to confirmed, once the consult is confirmed, it will collect all the updated data from the database and return
        it in a JSON Response, since the agenda will be updated asynchronously.It takes two arguments,
        'request' which expects a request object and 'pk' which expects a consult.pk key.

        *Note: the collection of appointments from user with Assistant roll, is based on the indexing syntax, since assistants
         can only be linked to a single doctor, this before we build up the multiple linking functionality in future updates.*
    """
    if request.user.roll == 'DOCTOR':
        aimed_user = request.user
    else:
        aimed_user = request.user.assistant.doctors.all()[0]

    consult = BaseConsult.objects.get(pk=pk)
    consult.status = 'CONFIRMED'
    consult.save()
    today = timezone.localtime().date()
    tzone = timezone.get_current_timezone()
    form = AgendaDateFilterForm
    consults_list = BaseConsult.objects.filter(created_by=aimed_user, datetime__date__gte=today, medical_status=False).order_by('datetime')
    months_names = collect_months_names(consults_list, tzone)
    data = {'html': render_to_string('appointments/partial_agenda_list.html', {'appointments': consults_list, 'months': months_names, 'form': form}, request=request)}
    data['to'] = request.user.username if request.user.roll == 'DOCTOR' else request.user.assistant.doctors.all()[0].username
    data['patient'] = consult.patient.first_names + ' ' + consult.patient.last_names
    data['datetime'] = consult.datetime.strftime('%B %-d, %Y at %I:%M %p')
    return JsonResponse(data)


def cancel_appointment(request, pk):
    """
        DOCSTRING:
        The cancel_appointment() view is used to cancel any consult if needed, since this process will be done from the
        Agenda view, then we need to return the response in a JSON Format, for this we will make use of our render_to_
        string function and return the rendered template as a string, if the request.method is 'GET' then the template
        will be rendered as a form with the information of that consult, if the request.method is 'POST' then the consult
        will be cancelled, setting the status attribute to 'CANCELLED' and saved. Since we need to update the Agenda
        with the updated consults, we will collect them form the DB with the new data, and return it through a JSON
        response object. The agenda is divided into months, so we need to collect all the months in which there are
        consults pending for us, how can we do that? We call our collected_months function and we pass the updated_consults
        and tzone as parameters, finally we send our response in JSON Format so the agenda view can update this data.

        *Note: the collection of appointments from user with Assistant roll, is based on the indexing syntax, since assistants
         can only be linked to a single doctor, this before we build up the multiple linking functionality in future updates.*
    """
    if request.user.roll == 'DOCTOR':
        aimed_user = request.user
    else:
        aimed_user = request.user.assistant.doctors.all()[0]

    today = timezone.localtime().date()
    consult = BaseConsult.objects.get(pk=pk)
    tzone = timezone.get_current_timezone()
    form = AgendaDateFilterForm
    template = 'appointments/cancel_appointment.html'
    context = {'consult': consult}
    data = {'html': render_to_string(template, context, request)}
    if request.method == 'POST':
        consult.status = 'CANCELLED'
        consult.save()
        appointments_list = BaseConsult.objects.filter(created_by=aimed_user, datetime__date__gte=today, medical_status=False).order_by('datetime')
        months_names = collect_months_names(appointments_list, tzone)
        data = {'html': render_to_string('appointments/partial_agenda_list.html', {'appointments': appointments_list, 'months': months_names, 'form':form}, request=request)}
        data['to'] = request.user.username if request.user.roll == 'DOCTOR' else request.user.assistant.doctors.all()[0].username
        data['patient'] = consult.patient.first_names + ' ' + consult.patient.last_names
        data['datetime'] = consult.datetime.strftime('%B %-d, %Y at %I:%M %p')
    return JsonResponse(data)


def registers(request):
    """
        DOCSTRING:
        The registers() view is used to display all the appointments that have been scheduled, no matter if they were
        attended or not, they will always be displayed anyways, here you can see if they were never attended, cancelled,
        confirmed or updated. This consult will also call the 'check_delayed_consults' to close all the consults that were
        not attended the day before or days before the current date. If the request.method is 'GET' it will return all
        the appointments along with the filtering form, if the request.method is 'POST' then the filtering will be processed
        and if the filters were changed, it will perform the filtering, else it will return a custom error, as well if the
        filtering did not found any matches. The registers page will be updated asynchronously, so we will need to return
        these values in JSON Format. It takes a single argument: 'request' and expects a request object.

        *Note: the collection of appointments from user with Assistant roll, is based on the indexing syntax, since assistants
         can only be linked to a single doctor, this before we build up the multiple linking functionality in future updates.*
    """
    # loop.run_until_complete(check_delayed_consults(request.user))

    if request.user.roll == 'DOCTOR':
        aimed_user = request.user
    else:
        aimed_user = request.user.assistant.doctors.all()[0]

    today = timezone.localtime()
    consults_list = BaseConsult.objects.filter(created_by=aimed_user).order_by('-datetime')
    template = 'appointments/registers.html'
    form = RegisterFilterForm
    context = {'registers': consults_list, 'form': form, 'items': len(consults_list), 'today': today}
    return render(request, template, context)


def filter_registers(request):
    """
        This filter_registers() function is used to filter the registers belonging to this user, depending on the parameters values inside the
        request.GET dictionary, this function will collect the 'patient', 'month' and 'year' parameter values and convert
        them into a datetime object, this way we can filter the consults based on this values, finally we will return our response
        in JSON Format, this function also checks if the 'page' parameter is inside the querystring, if it is, then the page that
        will be rendered will be that one in the 'page' value, else the first page will be rendered.
    """

    if request.user.roll == 'DOCTOR':
        aimed_user = request.user
    else:
        aimed_user = request.user.assistant.doctors.all()[0]

    patient_query = request.GET.get('patient')
    month_query = request.GET.get('month')
    year_query = request.GET.get('year')
    consults_list = filter_conditional_results(aimed_user, cleaned_data={'patient': patient_query, 'month': month_query, 'year': year_query}).order_by('datetime')
    context = {'registers': consults_list}
    data = {'html': render_to_string('appointments/partial_registers.html', context, request)}
    return JsonResponse(data)
