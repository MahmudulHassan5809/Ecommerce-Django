from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path('', views.BlogHomeView.as_view(), name="blog_home"),
    path('single/<str:slug>/<int:pk>/',
         views.SinglePostView.as_view(), name="single_post")
]
