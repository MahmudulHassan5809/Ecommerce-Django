from decimal import Decimal
from django.conf import settings
from ecom.models import Product
from django.http import HttpResponse
from django.shortcuts import render, redirect


class Cart(object):

    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, action=None):
        """
        Add a product to the cart or update its quantity.
        """
        id = product.id
        newItem = True
        if str(product.id) not in self.cart.keys():

            if product.discount_price:
                p_price = product.discount_price
            else:
                p_price = product.price

            product_image = product.product_images.all().first()

            self.cart[product.id] = {
                'userid': self.request.user.id,
                'product_id': id,
                'name': product.title,
                'quantity': 1,
                'price': p_price,
                'image': product_image.image.url
            }
        else:
            newItem = True

            for key, value in self.cart.items():
                if key == str(product.id):

                    value['quantity'] = value['quantity'] + 1
                    newItem = False
                    self.save()
                    break
            if newItem == True:

                if product.discount_price:
                    p_price = product.discount_price
                else:
                    p_price = product.price

                product_image = product.product_images.all().first()

                self.cart[product.id] = {
                    'userid': self.request,
                    'product_id': product.id,
                    'name': product.title,
                    'quantity': 1,
                    'price': p_prices,
                    'image': product_image.image.url
                }

        self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def decrement(self, product):
        for key, value in self.cart.items():
            if key == str(product.id):

                value['quantity'] = value['quantity'] - 1
                if(value['quantity'] < 1):
                    return redirect('cart:cart_detail')
                self.save()
                break
            else:
                print("Something Wrong")

    def clear(self):
        # empty cart
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True
