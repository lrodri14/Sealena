"""
    This accounts_utilities.py file contains all the imports, variable definitions and the function definitions needed for
    the accounts app to perform correctly, it is composed of one variable definition,'domains' which is a dictionary containing
    all the most used smtp servers worldwide, this way every time a user is created if the account email meets these requirements
    some initial information will be filled, this file contains two function definitions.
"""
from django.utils.html import strip_tags
from accounts.tokens import generate_token
from accounts.models import CustomUser, UsersProfile, ContactRequest
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends.smtp import EmailBackend
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

from appointments.models import GeneralConsult, AllergyAndImmunologicalConsult, DentalConsult, NeurologicalConsult, \
                                GynecologicalConsult, OphthalmologyConsult, PsychiatryConsult, SurgicalConsult, UrologicalConsult

from appointments.forms import GeneralConsultCreationForm, AllergyAndImmunologicalConsultCreationForm, DentalConsultCreationForm, \
                                NeurologicalConsultCreationForm, GynecologicalConsultCreationForm, OphthalmologyConsultCreationForm, \
                                PsychiatryConsultCreationForm, SurgicalConsultCreationForm, UrologicalConsultCreationForm, \
                                UpdateGeneralConsultForm, UpdateAllergyAndImmunologicalConsultForm, UpdateDentalConsultForm, \
                                UpdateNeurologicalConsultForm, UpdateGynecologicalConsultForm, UpdateOphthalmologyConsultForm, \
                                UpdatePsychiatryConsultForm, UpdateSurgicalConsultForm, UpdateUrologicalConsultForm

speciality_mapping = {
    'A&I': {'model': AllergyAndImmunologicalConsult, 'creation_form': AllergyAndImmunologicalConsultCreationForm, 'updating_form': UpdateAllergyAndImmunologicalConsultForm},
    'DT': {'model': DentalConsult, 'creation_form': DentalConsultCreationForm, 'updating_form': UpdateDentalConsultForm},
    'IM': {'model': GeneralConsult, 'creation_form': GeneralConsultCreationForm, 'updating_form': UpdateGeneralConsultForm},
    'GM': {'model': GeneralConsult, 'creation_form': GeneralConsultCreationForm, 'updating_form': UpdateGeneralConsultForm},
    'NEU': {'model': NeurologicalConsult, 'creation_form': NeurologicalConsultCreationForm, 'updating_form': UpdateNeurologicalConsultForm},
    'O&G': {'model': GynecologicalConsult, 'creation_form': GynecologicalConsultCreationForm, 'updating_form': UpdateGynecologicalConsultForm},
    'OPH': {'model': OphthalmologyConsult, 'creation_form': OphthalmologyConsultCreationForm, 'updating_form': UpdateOphthalmologyConsultForm},
    'PED': {'model': GeneralConsult, 'creation_form': GeneralConsultCreationForm, 'updating_form': UpdateGeneralConsultForm},
    'PSY': {'model': PsychiatryConsult, 'creation_form': PsychiatryConsultCreationForm, 'updating_form': UpdatePsychiatryConsultForm},
    'SRG': {'model': SurgicalConsult, 'creation_form': SurgicalConsultCreationForm, 'updating_form': UpdateSurgicalConsultForm},
    'URO': {'model': UrologicalConsult, 'creation_form': UrologicalConsultCreationForm, 'updating_form': UpdateUrologicalConsultForm}
}


def send_welcome_email(user):
    """
        DOCSTRING:
        This send_welcome_email function is used to send emails to new users, it constructs a new email with content based
        on the user who has been created. The email is sent in HTML format, and as an alternative it's presented as plain
        text. We make use of the EmailMultiAlternatives class to create and send the email.
    """
    user_first_name = user.first_name
    roll = user.roll

    try:
        title = 'Mr.' if user.profile.gender == 'MASCULINE' else 'Ms.'
    except UsersProfile.DoesNotExist:
        title = ''

    context = {'title': title, 'first_name': user_first_name, 'roll': roll}
    template = 'accounts/welcome_email.html'
    html_content = render_to_string(template, context)
    plain_content = strip_tags(html_content)
    plain_content = plain_content[plain_content.find('Welcome'):]

    subject = 'Welcome to Sealena'
    receiver = user.email
    email = EmailMultiAlternatives(subject=subject, body=plain_content, to=[receiver])
    email.attach_alternative(html_content, 'text/html')
    email.content_subtype = 'html'
    email.send()


def send_verification_email(user, request):
    """
        DOCSTRING:
        The send_verification_email function is used to send an email for identity verification. It contains a token link
        accessed by the user which redirects to the verification page.
    """
    current_site = get_current_site(request)

    context = {'user': user,
               'domain': current_site,
               'uid': urlsafe_base64_encode(force_bytes(user.pk)),
               'token': generate_token.make_token(user)}
    template = 'accounts/verification_email.html'
    html_content = render_to_string(template, context)
    plain_content = strip_tags(html_content)
    plain_content = plain_content[plain_content.find('Hi'):]

    subject = 'Sealena - Email Verification'
    receiver = user.email
    email = EmailMultiAlternatives(subject=subject, body=plain_content, to=[receiver])
    email.attach_alternative(html_content, 'text/html')
    email.content_subtype = 'html'
    email.send()


def check_token_validity(uidb64, token):
    """
        DOCSTRING:
        This check_token_validity function is used to check if the token is valid or not expired, it will retrieve the
        user's id from the base64 encoded value inside the token to retrieve the existing user, the return value is a
        boolean, if the user exists and the token is valid, returns True.
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except Exception as e:
        user = None

    return user, generate_token.check_token(user, token)


def check_requests(user):
    """
        DOCSTRING: This check_requests function is used to check if there are any requests sent to a specific user.
    """
    if not ContactRequest.objects.filter(to_user=user):
        return False
    return True
