from django.contrib import admin
from django.contrib.auth import get_user_model
from adminsortable2.admin import SortableAdminMixin
from .models import Category, SubCategory, Product, ProductImage, LeadSection, Brand, WishList, CompareProduct
from .forms import ProductForm

from django.contrib.auth.models import User
from django.utils.html import escape, mark_safe

# Register your models here.
User = get_user_model()


class SubCategoryline(admin.StackedInline):
    model = SubCategory
    extra = 1
    exclude = ['slug']


class CategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'slug', 'add_subcategory', 'active',)
    search_fields = ('name',)
    list_filter = ('name',)
    exclude = ['slug']
    list_editable = ['active']
    inlines = [SubCategoryline]
    list_per_page = 20

    def add_subcategory(self, obj):
        return mark_safe(f'<a target="_blank" href="http://127.0.0.1:8000/admin/news/subcategory/add/?category={obj.id}">Add SubCategory</a>')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        id = request.GET.get('category')
        if db_field.name == 'category' and id:
            kwargs["queryset"] = Category.objects.filter(id=int(id))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category, CategoryAdmin)


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    exclude = ['slug']
    list_per_page = 20


admin.site.register(Brand, BrandAdmin)


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 0
    max_num = 5


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

    form = ProductForm
    list_display = ["title", "category",
                    "price", "active"]
    search_fields = ('title', 'slug', 'category__name',
                     'active', 'tags__name')
    list_filter = ['category__name', 'active']
    list_editable = ['active', ]
    exclude = ['slug']
    list_per_page = 20


admin.site.register(Product, ProductAdmin)


class LeadSectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_lead', 'second_lead', 'third_lead')

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else True

    list_per_page = 20


# Register your models here.
admin.site.register(LeadSection, LeadSectionAdmin)


class WishListAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
    search_fields = ('user__username', 'product__title')
    list_per_page = 20


admin.site.register(WishList, WishListAdmin)


class CompareProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
    search_fields = ('user__username', 'product__title')
    list_per_page = 20


admin.site.register(CompareProduct, CompareProductAdmin)
