from django.db import models
import uuid
from userauths.models import User
from shortuuid.django_fields import ShortUUIDField
from django.db.models.signals import post_save
import random

def generate_default_pin():
    return random.randint(1000, 9999)




ACCOUNT_STATUS = (
    ('active', 'Active'),
    ('in-active', 'In-active'),
    ('pending', 'Pending'),
)

MARITAL_STATUS = (
    ('married', 'Married'),
    ('single', 'Single'),
    ('other', 'Other')
)

GENDER_STATUS = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other')
)

NATIONALITY = (
    ('afghanistan', 'Afghanistan'),
    ('albania', 'Albania'),
    ('algeria', 'Algeria'),
    ('andorra', 'Andorra'),
    ('angola', 'Angola'),
    ('antigua and barbuda', 'Antigua and Barbuda'),
    ('argentina', 'Argentina'),
    ('armenia', 'Armenia'),
    ('australia', 'Australia'),
    ('austria', 'Austria'),
    ('azerbaijan', 'Azerbaijan'),
    ('bahamas', 'Bahamas'),
    ('bahrain', 'Bahrain'),
    ('bangladesh', 'Bangladesh'),
    ('barbados', 'Barbados'),
    ('belarus', 'Belarus'),
    ('belgium', 'Belgium'),
    ('belize', 'Belize'),
    ('benin', 'Benin'),
    ('bhutan', 'Bhutan'),
    ('bolivia', 'Bolivia'),
    ('bosnia and herzegovina', 'Bosnia and Herzegovina'),
    ('botswana', 'Botswana'),
    ('brazil', 'Brazil'),
    ('brunei', 'Brunei'),
    ('bulgaria', 'Bulgaria'),
    ('burkina faso', 'Burkina Faso'),
    ('burundi', 'Burundi'),
    ('cambodia', 'Cambodia'),
    ('cameroon', 'Cameroon'),
    ('canada', 'Canada'),
    ('central african republic', 'Central African Republic'),
    ('chad', 'Chad'),
    ('chile', 'Chile'),
    ('china', 'China'),
    ('colombia', 'Colombia'),
    ('comoros', 'Comoros'),
    ('congo', 'Congo'),
    ('costa rica', 'Costa Rica'),
    ('croatia', 'Croatia'),
    ('cuba', 'Cuba'),
    ('cyprus', 'Cyprus'),
    ('czech republic', 'Czech Republic'),
    ('denmark', 'Denmark'),
    ('djibouti', 'Djibouti'),
    ('dominica', 'Dominica'),
    ('dominican republic', 'Dominican Republic'),
    ('ecuador', 'Ecuador'),
    ('egypt', 'Egypt'),
    ('el salvador', 'El Salvador'),
    ('equatorial guinea', 'Equatorial Guinea'),
    ('eritrea', 'Eritrea'),
    ('estonia', 'Estonia'),
    ('ethiopia', 'Ethiopia'),
    ('fiji', 'Fiji'),
    ('finland', 'Finland'),
    ('france', 'France'),
    ('gabon', 'Gabon'),
    ('gambia', 'Gambia'),
    ('georgia', 'Georgia'),
    ('germany', 'Germany'),
    ('ghana', 'Ghana'),
    ('greece', 'Greece'),
    ('grenada', 'Grenada'),
    ('guatemala', 'Guatemala'),
    ('guinea', 'Guinea'),
    ('guinea-bissau', 'Guinea-Bissau'),
    ('guyana', 'Guyana'),
    ('haiti', 'Haiti'),
    ('honduras', 'Honduras'),
    ('hungary', 'Hungary'),
    ('iceland', 'Iceland'),
    ('india', 'India'),
    ('indonesia', 'Indonesia'),
    ('iran', 'Iran'),
    ('iraq', 'Iraq'),
    ('ireland', 'Ireland'),
    ('israel', 'Israel'),
    ('italy', 'Italy'),
    ('jamaica', 'Jamaica'),
    ('japan', 'Japan'),
    ('jordan', 'Jordan'),
    ('kazakhstan', 'Kazakhstan'),
    ('kenya', 'Kenya'),
    ('kiribati', 'Kiribati'),
    ('north korea', 'North Korea'),
    ('south korea', 'South Korea'),
    ('kosovo', 'Kosovo'),
    ('kuwait', 'Kuwait'),
    ('kyrgyzstan', 'Kyrgyzstan'),
    ('laos', 'Laos'),
    ('latvia', 'Latvia'),
    ('lebanon', 'Lebanon'),
    ('lesotho', 'Lesotho'),
    ('liberia', 'Liberia'),
    ('libya', 'Libya'),
    ('lithuania', 'Lithuania'),
    ('luxembourg', 'Luxembourg'),
    ('macedonia', 'Macedonia'),
    ('madagascar', 'Madagascar'),
    ('malawi', 'Malawi')
)

IDENTITY_TYPES = (
    ('national_id_card', 'National ID Card'),
    ('passport', 'Passport'),
    ('driver_license', 'Driver\'s License'),
    ('state_id', 'State ID'),
    ('birth_certificate', 'Birth Certificate'),
    ('social_security_card', 'Social Security Card'),
    ('green_card', 'Green Card'),
    ('employment_id', 'Employment ID'),
    ('student_id', 'Student ID'),
    ('health_insurance_card', 'Health Insurance Card'),
    ('voter_registration_card', 'Voter Registration Card'),
)


#Create your models here.
# def user_directory_path(instance, filename):
#     ext = filename.split(".")[-1]
#     filename = "%s_%s" % (instance.id, ext)
#     return "user_{0}/{1}".format(instance.user.id, filename)

class Account(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    account_number = ShortUUIDField(unique=True, length=10, max_length=25, prefix='130', alphabet="0123456789")
    account_id = ShortUUIDField(unique=True, length=10, max_length=25, prefix='DEX', alphabet="0123456789")
    red_code = ShortUUIDField(unique=True,length=10, max_length=20, alphabet='abcdefgh0123456789')
    account_status = models.CharField(max_length=100, choices=ACCOUNT_STATUS, default='in-active')
    pin_number = ShortUUIDField(length=4, max_length=4, alphabet="0123456789", default=generate_default_pin)
    date = models.DateTimeField(auto_now_add=True)
    kyc_submitted = models.BooleanField(default=False)
    kyc_confirmed = models.BooleanField(default=False)
    recommended_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='recomended')

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user}"
    
# - ShortUUIDField is a custom field in Django that generates a short, unique identifier (UUID) for a model instance.
# - Unique: ShortUUIDs are designed to be unique, making them suitable for use as primary keys or unique identifiers.
# - Here's an example of a UUID: 123e4567-e89b-12d3-a456-426614174000


class KYC(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account = models.OneToOneField(Account, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='kyc', default='default.jpg')
    maritial_status = models.CharField(choices=MARITAL_STATUS, max_length=40)
    gender = models.CharField(choices=GENDER_STATUS, max_length=50)
    identity_types = models.CharField(choices=IDENTITY_TYPES, max_length=200)
    identity_image = models.ImageField(upload_to='kyc', null=True, blank=True)
    date_of_birth = models.DateTimeField(auto_now_add=False)
    signature = models.ImageField(upload_to='kyc', ) 
    #email = models.EmailField(unique=False)
    # address
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    pincode = models.CharField(max_length=50)  
    # contact
    mobile_number = models.CharField(max_length=100)
    fax = models.CharField(max_length=1000)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"

    
def create_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user = instance)
    # without needing to explicitly save the Account object in the registerview function. The signal handling takes care of it!
post_save.connect(create_account, sender=User)

# - post_save is a signal that is sent after a model instance is saved. It's a way to execute custom code after a save operation has been performed.

# After the save is complete, Django automatically checks if any post_save signal receivers are connected. This is an internal mechanism in Django's signal dispatching system.

# Here's what happens:

# 1. After saving the model instance, Django's save_base() method calls post_save_signal() to send the post_save signal.
# 2. post_save_signal() checks if there are any receivers connected to the post_save signal for the current model (in this case, the User model).
# 3. If there are connected receivers, post_save_signal() dispatches the signal to those receivers.

# - sender: The model class that sent the signal (in this case, the User model).
# - instance: The actual saved User object (passed automatically by Django).
# - created: A boolean indicating whether the instance was created (True) or updated (False).
# - note: here we can name the parameter as we want but should not change the position.