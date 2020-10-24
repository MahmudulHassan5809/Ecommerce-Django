from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from .models import ContactUs


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        exclude = ('solved',)
