from distutils.log import Log
from django.utils import timezone
from django.urls import reverse_lazy
from django.shortcuts import render
from pip import List
from blog.forms import PostForm, CommentForm
from blog.models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView,DeleteView,)

# Create your views here.


class AboutView(TemplateView):
    template_name = 'about.html'


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    models = Post


class CreatePostView(CreateView, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    from_class = PostForm
    model = Post

class PostUpdateView(UpdateView, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    from_class = PostForm
    model = Post

class PostDeleteView(DeleteView, LoginRequiredMixin):
    model = Post
    success_url=reverse_lazy('post_list')

class DraftList(ListView,LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model=Post
    
    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')
    