# Generated by Django 3.1.6 on 2021-08-11 19:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Allergy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allergy_type', models.CharField(help_text='Allergy Type', max_length=100, verbose_name='Allergy')),
                ('created_by', models.ForeignKey(help_text='User by who this allergy was created', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Allergy',
                'verbose_name_plural': 'Allergies',
                'unique_together': {('allergy_type', 'created_by')},
            },
        ),
        migrations.CreateModel(
            name='InsuranceCarrier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(help_text='Insurance Carrier', max_length=100, verbose_name='Company')),
                ('country', models.CharField(choices=[('HND', 'Honduras'), ('NIC', 'Nicaragua')], default=None, help_text='Insurance Carrier origin', max_length=100, null=True, verbose_name='Country')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='insurance_carrier', to=settings.AUTH_USER_MODEL, verbose_name='created_by')),
            ],
            options={
                'verbose_name': 'Insurance Carrier',
                'verbose_name_plural': 'Insurance Carriers',
                'unique_together': {('company', 'created_by')},
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_number', models.CharField(blank=True, help_text='Provide you ID Card Number', max_length=20, null=True, verbose_name='ID Number')),
                ('first_names', models.CharField(help_text="Patient's Name", max_length=50, verbose_name="Patient's Name")),
                ('last_names', models.CharField(help_text="Patient's Last Name", max_length=50, verbose_name="Patient's Last Name")),
                ('gender', models.CharField(choices=[('F', 'Femenine'), ('M', 'Masculine'), ('O', 'Other')], help_text='Gender', max_length=20, null=True, verbose_name="Patient's Gender")),
                ('birthday', models.DateField(help_text='Patients date of birth', verbose_name="Patient's Birthday")),
                ('phone_number', models.CharField(blank=True, help_text='Phone Number', max_length=20, null=True, verbose_name='Phone Number')),
                ('email', models.EmailField(blank=True, help_text='Email', max_length=254, null=True, verbose_name="Patient's Email")),
                ('civil_status', models.CharField(choices=[('S', 'Single'), ('M', 'Married'), ('W', 'Widowed'), ('D', 'Divorced'), ('SP', 'Separated')], max_length=12)),
                ('origin', models.CharField(choices=[('AR', 'Argentina'), ('BR', 'Brazil'), ('BZ', 'Belize'), ('CA', 'Canada'), ('CL', 'Chile'), ('CO', 'Colombia'), ('CR', 'Costa Rica'), ('GT', 'Guatemala'), ('HN', 'Honduras'), ('MX', 'Mexico'), ('NI', 'Nicaragua'), ('PA', 'Panama'), ('SV', 'El Salvador'), ('US', 'United States')], max_length=50)),
                ('residence', models.CharField(choices=[('AR', 'Argentina'), ('BR', 'Brazil'), ('BZ', 'Belize'), ('CA', 'Canada'), ('CL', 'Chile'), ('CO', 'Colombia'), ('CR', 'Costa Rica'), ('GT', 'Guatemala'), ('HN', 'Honduras'), ('MX', 'Mexico'), ('NI', 'Nicaragua'), ('PA', 'Panama'), ('SV', 'El Salvador'), ('US', 'United States')], max_length=50)),
                ('date_created', models.DateField(blank=True, help_text='Date Created', null=True, verbose_name='Date Created')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
            ],
            options={
                'verbose_name': 'Patient',
                'verbose_name_plural': 'Patients',
            },
        ),
        migrations.CreateModel(
            name='InsuranceInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_insurance', models.CharField(blank=True, choices=[('MEDICAL', 'Medical')], help_text='Type of insurance', max_length=50, null=True, verbose_name='Insurance Type')),
                ('expiration_date', models.DateField(help_text="Insurance's Expiration Date", verbose_name='Expiration Date')),
                ('insurance_carrier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='patients.insurancecarrier', verbose_name='Insurance Carrier')),
                ('patient', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='insurance', to='patients.patient', verbose_name='Insurance Owner')),
            ],
            options={
                'verbose_name': 'Insurance Information',
                'verbose_name_plural': "Patient's Insurance Data",
            },
        ),
        migrations.CreateModel(
            name='Antecedent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('antecedent', models.CharField(blank=True, help_text='Antecedent Type', max_length=150, null=True, verbose_name='Antecedent')),
                ('info', models.TextField(blank=True, help_text='About this antecedent', null=True, verbose_name='Antecedent Information')),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='antecedent_information', to='patients.patient', verbose_name='Patient')),
            ],
            options={
                'verbose_name': 'Antecedent',
                'verbose_name_plural': 'Antecedents',
            },
        ),
        migrations.CreateModel(
            name='AllergyInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about', models.TextField(blank=True, null=True, verbose_name='About Allergy')),
                ('allergy_type', models.ForeignKey(blank=True, help_text='Allergy type of the patient', null=True, on_delete=django.db.models.deletion.CASCADE, to='patients.allergy', verbose_name='Allergy Type')),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='allergy_information', to='patients.patient', verbose_name='Patient')),
            ],
            options={
                'verbose_name': 'Allergy Information',
                'verbose_name_plural': "Patient's Allergic Information",
            },
        ),
    ]
