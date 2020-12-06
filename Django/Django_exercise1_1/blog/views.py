from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Post, Category
from django.contrib.auth import login, logout, authenticate
from .forms import UserRegistrationForm


def home(request):
    return render(request, 'blog/home.html')


def posts(request):
    my_posts = Post.objects.all()
    context = {"posts": my_posts}
    return render(request, 'blog/posts.html', context)


def categories(request, pk):
    my_post = Post.objects.filter(category__slug=pk)
    context = {"posts": my_post}
    return render(request, 'blog/category.html', context)


def single_post(request, pk):
    my_post = Post.objects.get(slug=pk)
    context = {"post": my_post}
    return render(request, 'blog/single_post.html', context)


def login_view(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(request, username=username, password=password)
        print(username)
        if user:
            login(request, user)
            return redirect('home')
    else:
        return render(request, 'blog/login.html', context={})


def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            user = User.objects.create(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
            user.set_password(password)
            user.save()
            print('valid')
        else:
            print('invalid')
        context = {'form': form}
    else:
        form = UserRegistrationForm()
        context = {'form': form}
    return render(request, 'blog/register.html', context)
