from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages, auth
from django.views.decorators.http import require_POST
from django.contrib import messages
from .cart import Cart
from cart.models import Order, TransactionMethod
from ecom.models import Product
from .forms import OrderForm

# Create your views here.


@login_required(login_url="accounts:login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    messages.success(request, 'Product Added To Cart')
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


class CheckOut(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        order_form = OrderForm()
        context = {
            'title': 'Check Out',
            'order_form': order_form
        }
        return render(request, 'cart/check_out.html', context)

    def post(self, request, *args, **kwargs):
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            cart = Cart(request)
            total_bill = 0.0
            for key, value in request.session['cart'].items():
                total_bill = total_bill + \
                    (float(value['price']) * value['quantity'])

            payment_obj = get_object_or_404(
                TransactionMethod, id=int(request.POST.get('payment_option')))

            address = order_form.cleaned_data.get('address')
            phone_number = order_form.cleaned_data.get('phone_number')
            city = order_form.cleaned_data.get('city')
            zip_code = order_form.cleaned_data.get('zip_code')

            order = Order.objects.create(
                owner=request.user, total_bill=total_bill, payment_option=payment_obj, address=address, phone_number=phone_number, city=city, zip_code=zip_code)

            for key, value in request.session['cart'].items():
                order.products.add(int(value['product_id']))

            product_count = ''
            for key, value in request.session['cart'].items():
                product_count += f"{value['name']} --> {value['quantity']}"

            order.product_count = product_count

            product_price = ''
            for key, value in request.session['cart'].items():
                price = (float(value['price']) * value['quantity'])
                product_price += f"{value['name']} --> {value['quantity']} : {price} "

            order.product_price = product_price

            order.save()
            cart.clear()
            messages.success(request, 'Your Order Has Been Submitted')
            return redirect('cart:check_out')
        else:
            context = {
                'title': 'Check Out',
                'order_form': order_form
            }
            return render(request, 'cart/check_out.html', context)
