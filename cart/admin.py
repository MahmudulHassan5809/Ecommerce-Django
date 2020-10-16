from django.contrib import admin
from .models import Order, TransactionMethod

# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ["owner", "completed", "ordered_products",
                    "product_count", "product_price", "total_bill", "paid"]
    search_fields = ('owner__username', 'completed',)
    list_filter = ['completed', 'paid']
    list_editable = ['completed', 'paid']
    list_per_page = 20


admin.site.register(Order, OrderAdmin)


@admin.register(TransactionMethod)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('method_name', 'account_number', 'active')
    search_fields = ('method_name', 'account_number',)
    list_filter = ('active',)
    list_per_page = 20
