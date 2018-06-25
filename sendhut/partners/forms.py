from django import forms
from .models import Partner


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
