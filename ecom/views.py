from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
import datetime
from django.utils.timezone import now, localtime
import urllib.parse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import LeadSection, Product, Category, Brand
from .forms import BrandForm, PriceRangeForm, SizeChoiceForm
from django.views import View, generic
from django.db.models import Max, Min , Count , Sum
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


class CategoryView(View):
    def get(self, request, *args, **kwargs):
        cat_id = kwargs.get('id')
        category_name = urllib.parse.unquote(kwargs.get('slug'))

        category_obj = get_object_or_404(Category, id=cat_id)

        products = Product.objects.filter(active=True, category=category_obj)

        products = data_paginator(request, products)

        

        price_range = PriceRangeForm()
        brand_form = BrandForm()
        size_form = SizeChoiceForm()

        if True:
            val  = request.GET.get('defult')
            if val == "1":
                products = Product.objects.filter(active=True, category=category_obj).order_by('-created_at')

        if price_range:
            price_value = request.GET.get('price_range')
            brand_value = request.GET.get('name')
            size_value = request.GET.get('size')

            if price_value == "0":
                products = Product.objects.filter(active=True, category=category_obj, brand__id = brand_value)
            if price_value == "1":
                products = Product.objects.filter(active=True, category=category_obj,price__range = (0, 500) , brand__id = brand_value)
            if price_value == "2":
                products = Product.objects.filter(active=True, category=category_obj,price__range = (0, 1000) , brand__id = brand_value)
            if price_value == "3":
                products = Product.objects.filter(active=True, category=category_obj,price__range = (0, 5000) , brand__id = brand_value)
            if price_value == "4":
                products = Product.objects.filter(active=True, category=category_obj,price__range = (0, 500000) , brand__id = brand_value)
        context = {
            'title': category_obj.name.title(),
            'category_obj': category_obj,
            'products': products,
            'brand_form': brand_form,
            'price_range': price_range,
            'size_form': size_form
        }

        return render(request, 'ecom/category_products.html', context)


def data_paginator(request, product_list):
    page = request.GET.get('page', 1)

    paginator = Paginator(product_list, 10)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return products
