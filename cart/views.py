from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages, auth
from django.views.decorators.http import require_POST
from django.contrib import messages
from .cart import Cart
from cart.models import Order
from ecom.models import Product

# Create your views here.


@login_required(login_url="accounts:login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("ecom:home")


@login_required(login_url="accounts:login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart:cart_detail")


@login_required(login_url="auth:login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart:cart_detail")


@login_required(login_url="auth:login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart:cart_detail")


@login_required(login_url="/users/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart:cart_detail")


class CartDetail(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {
            'title': 'Cart View'
        }
        return render(request, 'cart/cart_detail.html', context)