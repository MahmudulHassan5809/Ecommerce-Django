from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from django.urls import reverse_lazy
from django.views.generic.base import TemplateView

app_name = "ecom"
urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('category/<str:category_slug>/<int:category_id>/',
         views.CategoryView.as_view(), name="category_view"),

    path('category/product/filter/<int:category_id>/',
         views.CategoryFilterView.as_view(), name='category_filter'),

    path('search/product/',
         views.CategoryFilterView.as_view(), name='search_product')
]
