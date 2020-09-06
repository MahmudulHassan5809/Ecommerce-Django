from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from django.urls import reverse_lazy
from django.views.generic.base import TemplateView

app_name = "ecom"
urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('category/<str:slug>/<int:id>/', views.CategoryView.as_view(), name="category_view"),
]
