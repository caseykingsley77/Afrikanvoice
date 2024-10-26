# blog/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Category
from .forms import PostForm, CategoryForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator


def post_list(request):
    posts = Post.objects.all()
    categories = Category.objects.all()
    
    # Paginate posts: 9 posts per page
    paginator = Paginator(posts, 2)  # Show 9 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog/post_list.html', {'page_obj': page_obj, 'categories': categories})


# View to list posts by category
def posts_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category)
    return render(request, 'blog/posts_by_category.html', {'category': category, 'posts': posts})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/add_post.html', {'form': form})

@login_required
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            return redirect('post_list')
    else:
        form = CategoryForm()
    return render(request, 'blog/add_category.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, DeleteUserForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse

# User Registration View
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            return redirect('post_list')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})

# User Profile View
@login_required
def profile(request):
    return render(request, 'blog/profile.html')

# User Profile Edit View
@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
    return render(request, 'blog/edit_profile.html', {'user_form': user_form})

# User Account Delete View
@login_required
def delete_profile(request):
    if request.method == 'POST':
        form = DeleteUserForm(request.POST)
        if form.is_valid() and form.cleaned_data['confirm_delete']:
            request.user.delete()
            messages.success(request, 'Your account has been deleted.')
            return redirect('post_list')
    else:
        form = DeleteUserForm()
    return render(request, 'blog/delete_profile.html', {'form': form})