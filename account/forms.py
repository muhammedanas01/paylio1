from django import forms
from account.models import KYC
from django.forms import ImageField, FileInput, DateInput

# class CustomeDateInput(forms.DateInput):
#     input_type = 'date'
#     placeholder = 'YYYY-MM-DD'

class KYCForm(forms.ModelForm):
    identity_image = ImageField(widget=FileInput)
    image = ImageField(widget=FileInput)
    signature = ImageField(widget=FileInput)
    date_of_birth = forms.DateField(widget=DateInput (attrs={'placeholder': 'YYYY-MM-DD'}))

    class Meta:
        model = KYC
        fields = [
            'full_name',
            'image',
            'maritial_status',
            'gender',
            'identity_types',
            'identity_image',
            'date_of_birth',
            'signature',
            'country',
            'state',
            'district',
            'pincode',
            'mobile_number',
            'fax',  
        ]

        widget = {
            'full_name': forms.TextInput( attrs={'placeholder': 'Full Name'} ),
            'mobile_number': forms.TextInput( attrs={'placeholder': 'Mobile Number'} ),
            'fax': forms.TextInput( attrs={'placeholder': 'Fax Number'} ), 
            'country': forms.TextInput( attrs={'placeholder': 'Country'} ),
            'state': forms.TextInput( attrs={'placeholder': 'State'} ),
            'district': forms.TextInput( attrs={'placeholder': 'District'} ),
        }

    
    


