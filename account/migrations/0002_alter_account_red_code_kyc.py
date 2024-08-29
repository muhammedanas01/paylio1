# Generated by Django 5.0.1 on 2024-07-16 19:27

import django.db.models.deletion
import shortuuid.django_fields
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='red_code',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='abcdefgh0123456789', length=10, max_length=20, prefix='', unique=True),
        ),
        migrations.CreateModel(
            name='KYC',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('full_name', models.CharField(max_length=1000)),
                ('image', models.ImageField(default='default.jpg', upload_to='kyc')),
                ('maritial_status', models.CharField(choices=[('married', 'Married'), ('single', 'Single'), ('other', 'Other')], max_length=40)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=50)),
                ('identity_types', models.CharField(choices=[('national_id_card', 'National ID Card'), ('passport', 'Passport'), ('driver_license', "Driver's License"), ('state_id', 'State ID'), ('birth_certificate', 'Birth Certificate'), ('social_security_card', 'Social Security Card'), ('green_card', 'Green Card'), ('employment_id', 'Employment ID'), ('student_id', 'Student ID'), ('health_insurance_card', 'Health Insurance Card'), ('voter_registration_card', 'Voter Registration Card')], max_length=200)),
                ('date_of_birth', models.DateTimeField()),
                ('signature', models.ImageField(upload_to='kyc')),
                ('country', models.CharField(choices=[('afghanistan', 'Afghanistan'), ('albania', 'Albania'), ('algeria', 'Algeria'), ('andorra', 'Andorra'), ('angola', 'Angola'), ('antigua and barbuda', 'Antigua and Barbuda'), ('argentina', 'Argentina'), ('armenia', 'Armenia'), ('australia', 'Australia'), ('austria', 'Austria'), ('azerbaijan', 'Azerbaijan'), ('bahamas', 'Bahamas'), ('bahrain', 'Bahrain'), ('bangladesh', 'Bangladesh'), ('barbados', 'Barbados'), ('belarus', 'Belarus'), ('belgium', 'Belgium'), ('belize', 'Belize'), ('benin', 'Benin'), ('bhutan', 'Bhutan'), ('bolivia', 'Bolivia'), ('bosnia and herzegovina', 'Bosnia and Herzegovina'), ('botswana', 'Botswana'), ('brazil', 'Brazil'), ('brunei', 'Brunei'), ('bulgaria', 'Bulgaria'), ('burkina faso', 'Burkina Faso'), ('burundi', 'Burundi'), ('cambodia', 'Cambodia'), ('cameroon', 'Cameroon'), ('canada', 'Canada'), ('central african republic', 'Central African Republic'), ('chad', 'Chad'), ('chile', 'Chile'), ('china', 'China'), ('colombia', 'Colombia'), ('comoros', 'Comoros'), ('congo', 'Congo'), ('costa rica', 'Costa Rica'), ('croatia', 'Croatia'), ('cuba', 'Cuba'), ('cyprus', 'Cyprus'), ('czech republic', 'Czech Republic'), ('denmark', 'Denmark'), ('djibouti', 'Djibouti'), ('dominica', 'Dominica'), ('dominican republic', 'Dominican Republic'), ('ecuador', 'Ecuador'), ('egypt', 'Egypt'), ('el salvador', 'El Salvador'), ('equatorial guinea', 'Equatorial Guinea'), ('eritrea', 'Eritrea'), ('estonia', 'Estonia'), ('ethiopia', 'Ethiopia'), ('fiji', 'Fiji'), ('finland', 'Finland'), ('france', 'France'), ('gabon', 'Gabon'), ('gambia', 'Gambia'), ('georgia', 'Georgia'), ('germany', 'Germany'), ('ghana', 'Ghana'), ('greece', 'Greece'), ('grenada', 'Grenada'), ('guatemala', 'Guatemala'), ('guinea', 'Guinea'), ('guinea-bissau', 'Guinea-Bissau'), ('guyana', 'Guyana'), ('haiti', 'Haiti'), ('honduras', 'Honduras'), ('hungary', 'Hungary'), ('iceland', 'Iceland'), ('india', 'India'), ('indonesia', 'Indonesia'), ('iran', 'Iran'), ('iraq', 'Iraq'), ('ireland', 'Ireland'), ('israel', 'Israel'), ('italy', 'Italy'), ('jamaica', 'Jamaica'), ('japan', 'Japan'), ('jordan', 'Jordan'), ('kazakhstan', 'Kazakhstan'), ('kenya', 'Kenya'), ('kiribati', 'Kiribati'), ('north korea', 'North Korea'), ('south korea', 'South Korea'), ('kosovo', 'Kosovo'), ('kuwait', 'Kuwait'), ('kyrgyzstan', 'Kyrgyzstan'), ('laos', 'Laos'), ('latvia', 'Latvia'), ('lebanon', 'Lebanon'), ('lesotho', 'Lesotho'), ('liberia', 'Liberia'), ('libya', 'Libya'), ('lithuania', 'Lithuania'), ('luxembourg', 'Luxembourg'), ('macedonia', 'Macedonia'), ('madagascar', 'Madagascar'), ('malawi', 'Malawi')], max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('pincode', models.CharField(max_length=50)),
                ('mobile_number', models.CharField(max_length=100)),
                ('fax', models.CharField(max_length=1000)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]