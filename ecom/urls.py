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
         views.CategoryFilterView.as_view(), name='search_product'),

    path('product/detail/<str:product_slug>/<int:pk>/',
         views.ProductDetailView.as_view(), name='product_detail'),


    path('add-wishlist/<int:product_id>/',
         views.AddWishListView.as_view(), name='add_wishlist'),
    path('remove-wishlist/<int:product_id>/',
         views.RemoveWishListView.as_view(), name='remove_wishlist'),

    path('add-compare/<int:product_id>/',
         views.AddCompareView.as_view(), name='add_compare'),
    path('remove-compare/<int:product_id>/',
         views.RemoveCompareView.as_view(), name='remove_compare'),

    path('product/rating/<int:product_id>/',
         views.ProductReviewView.as_view(), name='product_review')

]
