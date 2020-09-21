from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.template.loader import render_to_string
import datetime
from django.utils.timezone import now, localtime
import urllib.parse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import LeadSection, Product, Category, Brand, WishList, CompareProduct
from .forms import CategoryFilterForm
from django.views import View, generic
from accounts.mixins import AictiveUserRequiredMixin
from django.contrib import messages
from django.db.models import Max, Min, Count, Sum
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
        cat_id = kwargs.get('category_id')
        category_name = urllib.parse.unquote(kwargs.get('category_slug'))

        category_obj = get_object_or_404(Category, id=cat_id)

        products = Product.objects.filter(active=True, category=category_obj)

        products = data_paginator(request, products)

        print(products, '==============')

        category_filter_form = CategoryFilterForm()

        context = {
            'title': category_obj.name.title(),
            'category_obj': category_obj,
            'products': products,
            'category_filter_form': category_filter_form,
        }

        return render(request, 'ecom/category_products.html', context)


class CategoryFilterView(View):
    def get(self, request, *args, **kwargs):
        if kwargs.get('category_id'):
            cat_id = kwargs.get('category_id')
            search_category = cat_id
        elif request.GET.get('search_category') and request.GET.get('search_category') != '0':
            search_category = request.GET.get('search_category')
            cat_id = search_category
        else:
            return redirect('ecom:home')

        category_obj = get_object_or_404(Category, id=cat_id)

        products = Product.objects.active_filter().filter(category=category_obj)

        if request.GET.get('query') and request.GET.get('query') != '':
            query = request.GET.get('query')
            products = products.title_desc_filter(query)
        else:
            query = ''

        sub_cat = request.GET.get('sub_category')
        if sub_cat and sub_cat != '0':
            products = products.subcat_filter(sub_cat)

        category_filter_form = CategoryFilterForm(request.GET)

        if category_filter_form.is_valid():
            data = category_filter_form.cleaned_data
            brand = request.GET.get('brand_name')
            size = request.GET.get('size')
            price = data['price_range']
            new_or_popular = data['new_or_popular']

            if price:
                if price != '0':
                    if price == 'inf':
                        products = products.price_filter(0, 5000)
                    else:
                        products = products.price_filter(int(price))
            if brand:
                products = products.brand_filter(brand)

            if size != '0' and size:
                products = products.size_filter(size)

            if new_or_popular == 'new':
                products = products.newest_filter()
        else:
            print('not valid')

        products = data_paginator(request, products)

        context = {
            'title': category_obj.name.title(),
            'category_obj': category_obj,
            'products': products,
            'category_filter_form': category_filter_form,
            'search_category': search_category,
            'query': query
        }

        # html = render_to_string('ecom/products.html', context)
        # return JsonResponse(html, safe=False)

        return render(request, 'ecom/category_products.html', context)


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'ecom/single_product.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = self.object.title
        return context


class AddWishListView(AictiveUserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        product_obj = get_object_or_404(Product, id=product_id)

        check_wishlist = WishList.objects.filter(product=product_obj).first()

        if not check_wishlist:
            WishList.objects.create(user=request.user, product=product_obj)
            messages.success(request, 'Product Added Successfully To Wishlist')
        else:
            messages.warning(request, 'Product Already In  Wishlist')
        return redirect('accounts:my_wishlist')


class RemoveWishListView(AictiveUserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        product_obj = get_object_or_404(Product, id=product_id)

        WishList.objects.filter(product=product_obj).delete()
        messages.success(request, 'Product Removed From Wishlist')
        return redirect('accounts:my_wishlist')


class AddCompareView(AictiveUserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        product_obj = get_object_or_404(Product, id=product_id)

        check_compare = CompareProduct.objects.filter(
            product=product_obj).first()

        if not check_compare:
            CompareProduct.objects.create(
                user=request.user, product=product_obj)
            messages.success(request, 'Product Added Successfully To Compare')
        else:
            messages.warning(request, 'Product Already In  Comparelist')
        return redirect('accounts:my_comparelist')


class RemoveCompareView(AictiveUserRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        product_obj = get_object_or_404(Product, id=product_id)

        CompareProduct.objects.filter(product=product_obj).delete()
        messages.success(request, 'Product Removed From Compare')
        return redirect('accounts:my_comparelist')


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
