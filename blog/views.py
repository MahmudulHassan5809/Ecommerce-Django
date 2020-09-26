from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
import datetime
from django.utils.timezone import now, localtime
import urllib.parse
from .models import Category, Post
from django.views import View, generic
from django.contrib import messages


# Create your views here.
class BlogHomeView(generic.ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'post_list'
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(active=True)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Our Blog'
        context['categories'] = Category.objects.all()
        context['recent_posts'] = self.get_queryset(
        ).order_by('-created_at')[0:3]
        return context


class SinglePostView(generic.DetailView):
    model = Post
    template_name = 'blog/single.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        context['categories'] = Category.objects.all()
        context['recent_posts'] = Post.objects.filter(
            active=True).order_by('-created_at')[0:3]
        context['related_posts'] = Post.objects.filter(
            active=True, category=self.object.category)[0:3]
        return context
