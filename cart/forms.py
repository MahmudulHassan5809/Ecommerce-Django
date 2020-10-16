from django import forms
from django.forms import FileInput
from django.forms import ModelForm
from .models import Order, TransactionMethod


class OrderForm(ModelForm):
    CHOICES = (
        ('1', 'Direct Bank Tranfer'),
        ('2', 'Cash On Delivery')
    )
    payment_option = forms.ModelChoiceField(label='', queryset=TransactionMethod.objects.all(), required=True, widget=forms.RadioSelect(
        attrs={'class': 'Radio'}))

    class Meta:
        model = Order
        fields = ('address', 'phone_number', 'city', 'zip_code')
