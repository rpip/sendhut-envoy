from django import forms

from . import DeliveryVolumes
from .models import Partner, Merchant


class PartnerForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Your first name'}))
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Your last name'}))
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Your mobile phone number'}))
    email = forms.EmailField(
         max_length=40,
         widget=forms.TextInput(attrs={'placeholder': 'e.g. name@example.com'}),
    )

    class Meta:
        model = Partner
        fields = ['first_name', 'last_name', 'email', 'phone']


class MerchantForm(forms.ModelForm):
    name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Your name'}))
    business_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Your last name'}))
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Your mobile phone number'}))
    delivery_volume = forms.ChoiceField(choices=DeliveryVolumes.CHOICES)

    class Meta:
        model = Merchant
        fields = ['name', 'business_name', 'phone', 'delivery_volume']
