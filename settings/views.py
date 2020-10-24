from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import View, generic

from .models import ContactUs, AboutUs
from .forms import ContactUsForm
# Create your views here.


class ContactUsView(SuccessMessageMixin, generic.CreateView):
    model = ContactUs
    template_name = 'settings/contact_us.html'
    form_class = ContactUsForm
    success_url = reverse_lazy('settings:contact_us')
    success_message = "Thanks For You Message Our Team Will Contact With You Very Soon"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contact Us'
        return context


class AboutUsView(generic.TemplateView):
    template_name = 'settings/about_us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'About Us'
        context['about_us'] = AboutUs.objects.all().first()
        return context
