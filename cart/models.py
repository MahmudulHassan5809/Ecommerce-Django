from django.db import models
from django.contrib.auth import get_user_model
from ecom.models import Product

User = get_user_model()


class Order(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_orders')
    products = models.ManyToManyField(Product, related_name='product_orders')
    product_count = models.CharField(max_length=255)
    product_price = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    total_bill = models.FloatField()
    paid = models.BooleanField(default=False)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    payment_option = models.ForeignKey(
        "TransactionMethod", on_delete=models.CASCADE, related_name='payment_option_order')

    def ordered_products(self):
        return ",".join([str(p) for p in self.products.all()])


class TransactionMethod(models.Model):
    method_name = models.CharField(max_length=50)
    account_number = models.CharField(max_length=50)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.method_name}-{self.account_number}'
