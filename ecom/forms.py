from django import forms
from django.forms import FileInput
from django.forms import ModelForm
from .models import Product, ProductImage, Brand


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


class BrandForm(forms.ModelForm):
    name = forms.ModelMultipleChoiceField(
        label="Brand Name", widget=forms.CheckboxSelectMultiple, queryset=Brand.objects.all())

    class Meta:
        model = Brand
        exclude = ('slug',)

    def __init__(self, *args, **kwargs):
        super(BrandForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = ''
