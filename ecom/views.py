from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
import datetime
from django.utils.timezone import now, localtime
from .models import LeadSection, Product
from django.views import View, generic
# Create your views here.


class HomeView(View):
    def get(self, request, *args, **kwargs):
        first_lead_product = None
        second_lead_product = None
        third_lead_product = None

        first_lead = None
        second_lead = None
        third_lead = None

        try:
            first_lead = LeadSection.objects.select_related(
                'first_lead').only('first_lead').first()
            first_lead_product = Product.objects.select_related(
                'category', 'sub_category').prefetch_related('product_images').filter(active=True, category=first_lead.first_lead).order_by('-id')[:8]

            second_lead = LeadSection.objects.select_related(
                'second_lead').only('second_lead').first()
            second_lead_product = Product.objects.select_related(
                'category', 'sub_category').prefetch_related('product_images').filter(active=True, category=second_lead.second_lead).order_by('-id')[:8]

            third_lead = LeadSection.objects.select_related(
                'third_lead').only('third_lead').first()
            third_lead_product = Product.objects.select_related(
                'category', 'sub_category').prefetch_related('product_images').filter(active=True, category=third_lead.third_lead).order_by('-id')[:8]
        except Exception as e:
            pass

        today = datetime.date.today()
        today_products = Product.objects.select_related(
            'category', 'sub_category').prefetch_related('product_images').filter(active=True, created_at__gt=today)

        context = {
            'title': 'Home',
            'first_lead': first_lead,
            'first_lead_product': first_lead_product,
            'second_lead': second_lead,
            'second_lead_product': second_lead_product,
            'third_lead': third_lead,
            'third_lead_product': third_lead_product,
            'today_products': today_products
        }
        return render(request, 'ecom/home.html', context)
