from django import forms
from django.forms import FileInput
from django.forms import ModelForm
from .models import Product, ProductImage


class ProductForm(forms.ModelForm):
    SIZE_CHOICES = (
        ('0', 'XS'),
        ('1', 'Small'),
        ('2', 'Medium'),
        ('3', 'Large'),
        ('4', 'XL'),
        ('5', 'XXL'),
    )
    size = forms.MultipleChoiceField(
        choices=SIZE_CHOICES, widget=forms.SelectMultiple, required=False)

    class Meta:
        model = Product
        exclude = ('slug',)
