from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from.models import *
from.forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView, DeleteView
from django.db.models import Q


# Create your views here.

class Home(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_on')
        
        form = PostForm()
        context = {'posts':posts, 'form':form}
        return render(request, 'social/home.html', context)
    
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        posts = Post.objects.all().order_by('-created_on')
        if form.is_valid:
            var = form.save(commit=False)
            var.author = request.user
            var.save()
            return redirect('Home')
        else:
            messages.warning(request, 'Form invalid')
        context = {'var':form, 'posts':posts}
        return render(request, 'social/home.html', context)
    

class PostDetail(View, LoginRequiredMixin):
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        comments = Comment.objects.filter(post=post)
        form = CommentForm()
        context = {'post':post, 'form':form, 'comments':comments}
        return render(request, 'social/post.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        form = CommentForm(request.POST)
        post = Post.objects.get(pk=pk)
        if form.is_valid:
            var = form.save(commit=False)
            var.author = request.user
            var.post = post
            var.save()
            return redirect('Post', pk)
        else:
            pass

        comments = Comment.objects.filter(post=post)
        context = {'form':var, 'comments':comments, 'post':post}
        return render(request, 'social/post.html', context)


class PostEdit(LoginRequiredMixin, UserPassesTestMixin ,UpdateView):
    model = Post
    template_name = 'social/post_edit.html'
    fields = ['body']

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('Post', kwargs={'pk':pk})
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    

@login_required
def PrePostDelete(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'social/prepost_delete.html', context={'post':post})

@login_required
def PostDelete(request, pk):
    post = Post.objects.get(pk=pk)
    if post.author == request.user:
        post.delete()
        return redirect('Home')

@login_required
def LikePost(request, pk):
    post = Post.objects.get(pk=pk)
    if post.likes.filter(pk=request.user.pk):
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
            
    return redirect('Home')

@login_required
def disLikePost(request, pk):
    post = Post.objects.get(pk=pk)
    
    if post.dislikes.filter(pk=request.user.pk):
        post.dislikes.remove(request.user)
    else:
        post.dislikes.add(request.user)
    return redirect('Home')

@login_required
def SearchPost(request):
    search = request.GET['search']
    posts = Post.objects.filter(Q(author__username__icontains=search)|Q(body__icontains=search)|Q(created_on__icontains=search))
    context = {'posts':posts}
    return render(request, 'social/search.html', context)

@login_required
def deleteComment(request, pk):
    comment = Comment.objects.get(pk=pk)
    post = comment.post
    if request.user == comment.author:
        comment.delete()
        return redirect('Post', pk=post.pk)

    
