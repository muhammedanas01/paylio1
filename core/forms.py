from django import forms
from core.models  import CreditCard

class CreditCardForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"card holder name"}))
    number = forms.IntegerField(widget=forms.TextInput(attrs={"placeholder":"card number"}))
    month = forms.IntegerField(widget=forms.TextInput(attrs={"placeholder":"Expiry month"}))
    year = forms.IntegerField(widget=forms.TextInput(attrs={"placeholder":"Expiry year"}))
    cvv = forms.IntegerField(widget=forms.TextInput(attrs={"placeholder":"CVV"}))

    class Meta:
        model = CreditCard
        fields = ['name', 'number', 'month', 'year', 'cvv', 'month', 'year', 'card_type']