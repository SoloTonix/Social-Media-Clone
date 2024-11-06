from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import UpdateView
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from.models import *
from social.models import Post
from django.contrib.auth.decorators import login_required
# Create your views here.
class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'user/index.html')

profiles = UserProfile.objects.all()

@login_required
def FollowUser(request, pk):
    profile = profiles.get(pk=pk)
    profile.followers.add(request.user.pk)

    return redirect('Profile', pk=profile.pk)

@login_required
def UnfollowUser(request, pk):
    profile = profiles.get(pk=pk)
    profile.followers.remove(request.user.pk)

    return redirect('Profile', pk=profile.pk)


class UserProfile(View, LoginRequiredMixin):
    profile = UserProfile.objects.all()  
    def get(self, request, pk, *args, **kwargs):
        profile = self.profile.get(pk=pk)
        user = profile.user
        posts = Post.objects.filter(author=user)
        followers= profile.followers.count()
        context = {'profile':profile, 'posts':posts, 'followers':followers}

        return render(request, 'user/profile.html', context)
    

class PersonalProfile(View, LoginRequiredMixin, UserPassesTestMixin):
    def get(self, request, *args, **kwargs):
        return redirect('Profile', self.request.user.pk)
    
    def test_func(self):
        profile = profiles.get(pk=self.request.user.pk)
        return profile.user == self.request.user.pk
    


class UserProfileEdit(View, LoginRequiredMixin, UserPassesTestMixin):
    def get(self, request, *args, **kwargs):
        profile = profiles.get(pk=self.request.user.pk)
        form = UserProfileForm(request.GET or None, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('Profile', self.request.user.pk)
        form = UserProfileForm()

        context = {'form':form}
        return render(request, 'user/profile_edit.html', context)
    
    def test_func(self):
        profile = profiles.get(pk=self.request.user.pk)
        profile.user = self.request.user


def SignUp(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Index')
        else:
            messages.warning(request, 'Sorry something went wrong')
    else:
        form = RegistrationForm()
    context = {'form':form}
    return render(request, 'user/signup.html', context)

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            return redirect('Home')
        else:
            messages.warning(request, 'This user does not exist...')
            return redirect('Login')
        
    return render(request, 'user/login.html')


def Logout(request):
    logout(request)
    return redirect('Index')

