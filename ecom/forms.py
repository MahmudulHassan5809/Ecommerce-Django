from django import forms
from django.forms import FileInput
from django.forms import ModelForm
from .models import Product, ProductImage, Brand, ProductReview


SIZE_CHOICES = (
    ('0', '-----------'),
    ('xs', 'XS'),
    ('sm', 'Small'),
    ('md', 'Medium'),
    ('l', 'Large'),
    ('xl', 'XL'),
    ('xxl', 'XXL'),
)


class ProductForm(forms.ModelForm):
    size = forms.MultipleChoiceField(
        choices=SIZE_CHOICES, widget=forms.SelectMultiple, required=False)

    class Meta:
        model = Product
        exclude = ('slug',)


# class BrandForm(forms.ModelForm):
#     name = forms.ModelChoiceField(label="", queryset=Brand.objects.all())

#     class Meta:
#         model = Brand
#         exclude = ('slug',)

#     def __init__(self, *args, **kwargs):
#         super(BrandForm, self).__init__(*args, **kwargs)
#         self.fields['name'].label_classes = ('custom-control-label', )
#         # self.fields['name'].label = ''


# class PriceRangeForm(forms.Form):
#     PRICE_CHOICES = (
#         ('0', '-----------'),
#         ('1', 'Up To 500'),
#         ('2', 'Up To 1000'),
#         ('3', 'Up To 5000'),
#         ('4', 'Greater Than 5000'),
#     )

#     price_range = forms.ChoiceField(label="", choices=PRICE_CHOICES)


class CategoryFilterForm(forms.Form):
    NEW_POPULAR_CHOICES = (
        ('default', 'Default'),
        ('new', 'NEW'),
        ('popular', 'Popular'),
    )

    PRICE_CHOICES = (
        ('0', '-----------'),
        ('500', 'Up To 500'),
        ('1000', 'Up To 1000'),
        ('5000', 'Up To 5000'),
        ('inf', 'Greater Than 5000'),
    )

    brand_name = forms.ModelChoiceField(
        label="", queryset=Brand.objects.all(), required=False)
    size = forms.ChoiceField(label="", choices=SIZE_CHOICES, required=False)
    price_range = forms.ChoiceField(
        label="", choices=PRICE_CHOICES, required=False)
    new_or_popular = forms.ChoiceField(
        label='', choices=NEW_POPULAR_CHOICES, required=False, widget=forms.Select(attrs={"onChange": 'submit()'}))


class ProductReviewForm(forms.ModelForm):
    RATING_CHOICES = (
        ('--', 'Select Your Rating'),
        ('1', 'Very Low'),
        ('2', 'Low'),
        ('3', 'Medium'),
        ('4', 'Good'),
        ('5', 'Very Good'),
    )

    rating = forms.TypedChoiceField(
        choices=RATING_CHOICES, coerce=int,)
    name = forms.CharField(label='Your name', required=True)
    email = forms.EmailField(label='Your Email Address', required=True)

    class Meta:
        model = ProductReview
        exclude = ('user', 'product')
        widgets = {
            'review': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        if self.user.is_authenticated:
            self.fields["name"].initial = self.user.username
            self.fields["email"].initial = self.user.email
