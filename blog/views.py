from distutils import log
from distutils.log import Log
from django.utils import timezone
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from blog.forms import PostForm, CommentForm
from blog.models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView, DeleteView,)

# Create your views here.


class AboutView(TemplateView):
    template_name = 'about.html'


class PostListView(ListView):
    model = Post
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['count']=0
        for i in Comment.objects.all():
            if i.approved_comment==True:
                context['count']+=1
        return context
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post
    def id(request,pk):
        template_name='blog/post_detail.html'
        post = get_object_or_404(Post,pk=pk)
        

        

class CreatePostView(CreateView, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    from_class = PostForm
    model = Post
    fields=('author','title','text')


class PostUpdateView(UpdateView, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    from_class = PostForm
    fields=('author','title','text')
    model = Post


class PostDeleteView(DeleteView, LoginRequiredMixin):
    model = Post
    success_url = reverse_lazy('post_list')


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('create_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)

################################
################################

@login_required
def add_comment_to_post(request, pk):
    post=get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=post
            comment.save()
            return redirect('post_detail',pk=post.pk)
       
    else:
        form=CommentForm()
    return render(request,'blog/comment_form.html',{'form':form})

@login_required
def comment_approve(request, pk):
    comment=get_object_or_404(Comment,pk=pk)   
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment=get_object_or_404(Comment,pk=pk)
    post_pk=comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)