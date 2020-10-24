from django.urls import path
from . import views

app_name = "settings"
urlpatterns = [
    path('contact/', views.ContactUsView.as_view(), name="contact_us"),
    path('about/', views.AboutUsView.as_view(), name="about_us"),

]
