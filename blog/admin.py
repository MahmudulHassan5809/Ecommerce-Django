from django.contrib import admin
from .models import Category, Post
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    exclude = ['slug']
    list_per_page = 20


admin.site.register(Category, CategoryAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('category','title', 'active','created_at')
    search_fields = ('title','category__name')
    list_filter = ('active',)
    list_editable = ['active']
    exclude = ['slug']
    list_per_page = 20


admin.site.register(Post, PostAdmin)
