from django.shortcuts import render, HttpResponseRedirect,get_object_or_404, redirect
from django.urls import reverse, reverse_lazy

# VIEW
from django.views.generic import CreateView, ListView, DetailView, UpdateView, View, TemplateView, DeleteView

#Authentication
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

# Login MIXIN
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache


#forms
from .forms import PostForm
from django.contrib.auth.forms import AuthenticationForm

#models
from django.contrib.auth.models import User
from app_post.models import Post

#message
from django.contrib import messages

import uuid
from django.db.models import Q

#----------------------------------------------------------------

# Create your views here.
def home(request):
    
    posts = Post.all_posts()
    form  =PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            print("Form is valid")
            messages.success(request, 'Post created successfully')
            return redirect('home')  
    context = {
        'form': form,
        'posts':posts,
        }
    return render(request, 'app_post/home.html', context)