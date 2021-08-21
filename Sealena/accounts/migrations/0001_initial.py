# Generated by Django 3.1.6 on 2021-08-09 20:22

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('roll', models.CharField(choices=[('DOCTOR', 'Doctor'), ('ASSISTANT', 'Assistant')], help_text='Choose the roll you will acquire in this account.', max_length=25, verbose_name='Roll')),
                ('confirmed', models.BooleanField(default=False, help_text='Confirmed User Account', null=True, verbose_name='Confirmed?')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'ordering': ['username'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_message', models.TextField(blank=True, help_text="Chat's last message", null=True, verbose_name="Chat's last message")),
                ('last_message_sender', models.ForeignKey(blank=True, help_text='Last message sender', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Last message sender')),
                ('participants', models.ManyToManyField(blank=True, help_text='Chat Participants', related_name='participants', to=settings.AUTH_USER_MODEL, verbose_name='Participants')),
            ],
            options={
                'verbose_name': 'Chat',
                'verbose_name_plural': 'Chats',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(blank=True, help_text='Product ID', max_length=255, null=True, verbose_name='Product ID')),
                ('user_type', models.CharField(choices=[('DOCTOR', 'Doctor'), ('ASSISTANT', 'Assistant')], help_text='Product User Type', max_length=50, null=True, verbose_name='Product User Type')),
                ('plan', models.CharField(choices=[('PREMIUM', 'Premium')], help_text='Product Plan Type', max_length=50, null=True, verbose_name='Product Plan Type')),
                ('name_id', models.CharField(blank=True, help_text='Product Name ID', max_length=50, null=True, unique=True, verbose_name='Name ID')),
                ('name', models.CharField(blank=True, help_text='Product Name', max_length=50, null=True, unique=True, verbose_name='Name')),
                ('description', models.TextField(help_text='Product Description', null=True, verbose_name='Description')),
                ('product_type', models.CharField(choices=[('SERVICE', 'Service')], default='Service', help_text='Product Type', max_length=50, null=True, verbose_name='Type')),
                ('category', models.CharField(choices=[('SOFTWARE', 'Software')], default='Software', help_text='Product Category', max_length=50, null=True, verbose_name='Category')),
                ('image', models.ImageField(blank=True, help_text='Product Image', null=True, upload_to='', verbose_name='Image')),
                ('home_image', models.ImageField(blank=True, help_text='Product Image', null=True, upload_to='', verbose_name='Home Image')),
                ('get_product_url', models.URLField(blank=True, help_text='Get Product URL', null=True, verbose_name='Get Product URL')),
                ('edit_product_url', models.URLField(blank=True, help_text='Edit Product URL', null=True, verbose_name='Edit Product URL')),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.customuser')),
                ('speciality', models.CharField(blank=True, choices=[('A&I', 'Allergy & Immunology'), ('DT', 'Dentist'), ('IM', 'Internal Medicine'), ('GM', 'General Medicine'), ('NEU', 'Neurology'), ('O&G', 'Obstetrics & Gynecology'), ('OPH', 'Ophthalmology'), ('PED', 'Pediatrics'), ('PSY', 'Psychiatry'), ('SRG', 'Surgery'), ('URO', 'Urology')], help_text="Doctor's Speciality", max_length=100, verbose_name='Speciality')),
                ('linking_id', models.CharField(blank=True, help_text='Used by Assistants to link to Doctors', max_length=14, null=True, unique=True, verbose_name='Linking ID')),
                ('subscription', models.CharField(blank=True, choices=[('BASIC', 'Basic'), ('PREMIUM', 'Premium')], default='BASIC', help_text='Account Subscription Type', max_length=10, null=True, verbose_name='Subscription')),
            ],
            options={
                'verbose_name': 'Doctor',
                'verbose_name_plural': 'Doctors',
                'ordering': ['first_name'],
            },
            bases=('accounts.customuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UsersProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('availability', models.CharField(choices=[('A', 'Available'), ('B', 'Busy')], default='A', help_text='User Availability', max_length=50, null=True, verbose_name='Availability')),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='accounts/profile_pictures', verbose_name='Profile Picture')),
                ('bio', models.TextField(blank=True, help_text='Let us know about you', null=True, verbose_name='Biography')),
                ('gender', models.CharField(choices=[('MASCULINE', 'Masculine'), ('FEMENINE', 'Femenine')], max_length=25, null=True, verbose_name='Gender')),
                ('birth_date', models.DateField(help_text='Birth date', null=True, verbose_name='Birth Date')),
                ('origin', models.CharField(choices=[('AR', 'Argentina'), ('BR', 'Brazil'), ('BZ', 'Belize'), ('CA', 'Canada'), ('CL', 'Chile'), ('CO', 'Colombia'), ('CR', 'Costa Rica'), ('GT', 'Guatemala'), ('HN', 'Honduras'), ('MX', 'Mexico'), ('NI', 'Nicaragua'), ('PA', 'Panama'), ('SV', 'El Salvador'), ('US', 'United States')], max_length=50, null=True, verbose_name='Origin')),
                ('location', models.CharField(choices=[('AR', 'Argentina'), ('BR', 'Brazil'), ('BZ', 'Belize'), ('CA', 'Canada'), ('CL', 'Chile'), ('CO', 'Colombia'), ('CR', 'Costa Rica'), ('GT', 'Guatemala'), ('HN', 'Honduras'), ('MX', 'Mexico'), ('NI', 'Nicaragua'), ('PA', 'Panama'), ('SV', 'El Salvador'), ('US', 'United States')], help_text='Provide your location', max_length=100, null=True, verbose_name='Location')),
                ('address', models.TextField(blank=True, help_text='Provide your exact address', max_length=200, null=True, verbose_name='Address')),
                ('phone_number', models.CharField(blank=True, help_text='Provide your phone number', max_length=15, null=True, verbose_name='Phone Number')),
                ('block_list', models.ManyToManyField(blank=True, help_text="User's Block List", related_name='block_list', to=settings.AUTH_USER_MODEL, verbose_name='Block List')),
                ('contacts', models.ManyToManyField(blank=True, help_text='Contacts List', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'User Profile',
                'verbose_name_plural': 'User Profiles',
                'ordering': ['user'],
            },
        ),
        migrations.CreateModel(
            name='UserGeneralSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wallpaper', models.CharField(blank=True, help_text='Choose Wallpaper', max_length=100, null=True, verbose_name='Wallpaper')),
                ('sfx', models.BooleanField(blank=True, default=True, help_text='Sound Effects Switch', null=True, verbose_name='SFX')),
                ('notifications', models.BooleanField(blank=True, default=True, help_text='Notifications', null=True, verbose_name='Notifications')),
                ('user', models.OneToOneField(blank=True, help_text='User Settings', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='general_settings', to=settings.AUTH_USER_MODEL, verbose_name='User Settings')),
            ],
            options={
                'verbose_name': 'User General Setting',
                'verbose_name_plural': 'User General Settings',
            },
        ),
        migrations.CreateModel(
            name='UserAccountSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tzone', models.CharField(help_text='Provide your timezone', max_length=40, null=True, verbose_name='Timezone')),
                ('session_expire_time', models.IntegerField(blank=True, choices=[(300, '5 Minutes'), (600, '10 Minutes'), (1200, '20 Minutes'), (1800, '30 Minutes'), (3600, '1 Hour')], default=1800, help_text='Provide your session time expire timeout', null=True, verbose_name='Session Expire Time')),
                ('user', models.OneToOneField(blank=True, help_text='User Settings', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='account_settings', to=settings.AUTH_USER_MODEL, verbose_name='User Settings')),
            ],
            options={
                'verbose_name': 'User Account Setting',
                'verbose_name_plural': 'User Account Settings',
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscription_id', models.CharField(help_text='Subscription ID', max_length=255, null=True, verbose_name='Subscription ID')),
                ('user', models.ForeignKey(help_text='Subscription User', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subs', to=settings.AUTH_USER_MODEL, verbose_name='Subscription User')),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_plan_id', models.CharField(blank=True, help_text='Product Plan ID', max_length=255, null=True, verbose_name='Product ID')),
                ('user_type', models.CharField(blank=True, help_text='Product User Type', max_length=50, null=True, verbose_name='Product User Type')),
                ('plan', models.CharField(blank=True, help_text='Product Plan Type', max_length=50, null=True, verbose_name='Product Plan Type')),
                ('name_id', models.CharField(blank=True, help_text='Plan Name ID', max_length=50, null=True, unique=True, verbose_name='Name ID')),
                ('name', models.CharField(blank=True, help_text='Plan Name', max_length=50, null=True, unique=True, verbose_name='Name')),
                ('description', models.TextField(help_text='Plan Description', null=True, verbose_name='Description')),
                ('status', models.CharField(choices=[('CREATED', 'Created'), ('ACTIVE', 'Active'), ('INACTIVE', 'Inactive')], help_text='Plan Status', max_length=50, null=True, verbose_name='Status')),
                ('frequency', models.CharField(choices=[('MONTH', 'Monthly')], help_text='Plan Billing Frequency', max_length=50, null=True, verbose_name='Frequency')),
                ('price', models.CharField(help_text='Plan Price', max_length=5, null=True, verbose_name='Price')),
                ('tenure', models.CharField(choices=[('TRIAL', 'Trial'), ('REGULAR', 'Regular')], help_text='Plan Tenure', max_length=50, null=True, verbose_name='Tenure')),
                ('sequence', models.CharField(help_text='Plan Sequence', max_length=2, null=True, verbose_name='Sequence')),
                ('total_cycles', models.IntegerField(help_text='Cycles to be billed', null=True, verbose_name='Cycles')),
                ('auto_billing', models.BooleanField(help_text='Plan Billing Type', null=True, verbose_name='Auto Billing')),
                ('setup_fee', models.IntegerField(default=0, help_text='Setup Fee', null=True, verbose_name='Setup Fee')),
                ('setup_fee_failure_action', models.CharField(choices=[('CANCEL', 'Cancel'), ('CONTINUE', 'Continue')], help_text='Billing Failure Action', max_length=10, null=True, verbose_name='Billing Failure Action')),
                ('payment_failure_threshold', models.IntegerField(help_text='Payment Failure Threshold', null=True, verbose_name='Payment Failure Threshold')),
                ('get_plan_url', models.URLField(blank=True, help_text='Get Plan URL', null=True, verbose_name='Get Plan URL')),
                ('edit_plan_url', models.URLField(blank=True, help_text='Edit Plan URL', null=True, verbose_name='Edit Plan URL')),
                ('deactivate_plan_url', models.URLField(blank=True, help_text='Deactivate Plan URL', null=True, verbose_name='Deactivate Plan URL')),
                ('product', models.ForeignKey(help_text='Plan Product', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_plan', to='accounts.product', verbose_name='Plan Product')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(blank=True, help_text='Message time creation', null=True, verbose_name='datetime')),
                ('text', models.TextField(blank=True, help_text='Message Text', null=True, verbose_name='Text')),
                ('image', models.ImageField(blank=True, help_text='Message Image', null=True, upload_to='', verbose_name='Image')),
                ('status', models.CharField(blank=True, choices=[('UNREAD', 'Unread'), ('READ', 'Read')], default='UNREAD', help_text='Message Status', max_length=6, null=True, verbose_name='status')),
                ('chat', models.ForeignKey(blank=True, help_text='Chat', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message', to='accounts.chat', verbose_name='Chat')),
                ('created_by', models.ForeignKey(blank=True, help_text='Sender', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Sender')),
            ],
        ),
        migrations.CreateModel(
            name='MailingCredential',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('smtp_server', models.CharField(blank=True, default='', help_text='Provide the SMTP Server', max_length=100, null=True, verbose_name='SMTP Server')),
                ('port', models.IntegerField(blank=True, help_text='Provide the port used by your server', null=True, verbose_name='Port')),
                ('email', models.EmailField(blank=True, help_text='Provide your email', max_length=254, null=True, verbose_name='Email')),
                ('password', models.CharField(blank=True, help_text='Provide your password', max_length=254, null=True, verbose_name='Password')),
                ('use_tls', models.BooleanField(default=False, verbose_name='Use TLS? (Recommended)')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mailing_credentials', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Mailing Credential',
                'verbose_name_plural': 'Mailing Credentials',
            },
        ),
        migrations.CreateModel(
            name='ContactRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_user', models.ForeignKey(blank=True, help_text='User sending the request', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Request Sender')),
                ('to_user', models.ForeignKey(blank=True, help_text='User to send the request', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='request', to=settings.AUTH_USER_MODEL, verbose_name='Request Receive')),
            ],
            options={
                'verbose_name': 'Contact Request',
                'verbose_name_plural': 'Contact Requests',
                'unique_together': {('from_user', 'to_user')},
            },
        ),
        migrations.CreateModel(
            name='Assistant',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.customuser')),
                ('doctors', models.ManyToManyField(blank=True, help_text="Doctor's who this assistant will be working with", to='accounts.Doctor', verbose_name='Doctors')),
            ],
            options={
                'verbose_name': 'Assistant',
                'verbose_name_plural': 'Assistants',
                'ordering': ['first_name'],
            },
            bases=('accounts.customuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]