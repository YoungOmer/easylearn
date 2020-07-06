from django.contrib.auth.views import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login
from django.contrib import messages
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect



from accounts.models import User
from blog.models import Series, Blog
from .forms import RegisterForm, ProfileUpdate, BioUpdate
# Create your views here.


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            messages.success(request, f"you're welcome to ")
            return redirect('profile')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form':form})

@login_required
def profile(request):
    blog_list   =   Blog.objects.filter(author=request.user).order_by('-date_stamp')
    series_list =   Series.objects.filter(owner=request.user).order_by('-timestamp')
    form        =   BioUpdate(instance=request.user)
    if request.method == "POST":
        form           =   BioUpdate(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')

    context = {
        'series_list':  series_list,
        'blog_list':blog_list,
        'form':form
    }
    return render(request, 'accounts/profile.html', context )


    

@login_required
def profileUpdate(request):
    form = ProfileUpdate(instance=request.user)
    if request.method == "POST":
        form = ProfileUpdate(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, F"You have successfully Updated Your Profile")
            return redirect('profile')
    return render(request, 'accounts/profile_update.html', {'form':form})



class ProfileDetail(DetailView):
    model   =   User




@login_required
def passwordChangedView(request):
    if request.method == "POST":
        form    =   PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "you've successufully changed your password")
            return redirect("profile")
    else:
        form    =   PasswordChangeForm(request.user)
  
    return render(request, "accounts/password-change-form.html", {'form':form})

    