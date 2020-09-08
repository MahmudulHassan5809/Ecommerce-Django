from django import forms
from django.forms import FileInput
from django.forms import ModelForm
from .models import Product, ProductImage, Brand


SIZE_CHOICES = (
    ('0', 'XS'),
    ('1', 'Small'),
    ('2', 'Medium'),
    ('3', 'Large'),
    ('4', 'XL'),
    ('5', 'XXL'),
)


class ProductForm(forms.ModelForm):
    size = forms.MultipleChoiceField(
        choices=SIZE_CHOICES, widget=forms.SelectMultiple, required=False)

    class Meta:
        model = Product
        exclude = ('slug',)


class BrandForm(forms.ModelForm):
    name = forms.ModelChoiceField(label="", queryset=Brand.objects.all())

    class Meta:
        model = Brand
        exclude = ('slug',)

    def __init__(self, *args, **kwargs):
        super(BrandForm, self).__init__(*args, **kwargs)
        self.fields['name'].label_classes = ('custom-control-label', )
        # self.fields['name'].label = ''


class PriceRangeForm(forms.Form):
    PRICE_CHOICES = (
        ('0', '-----------'),
        ('1', 'Up To 500'),
        ('2', 'Up To 1000'),
        ('3', 'Up To 5000'),
        ('4', 'Greater Than 5000'),
    )

    price_range = forms.ChoiceField(label="", choices=PRICE_CHOICES)


class SizeChoiceForm(forms.Form):
    size = forms.ChoiceField(widget=forms.RadioSelect(), choices=SIZE_CHOICES)
