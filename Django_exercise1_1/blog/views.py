from django.shortcuts import render, redirect
from .models import Post, Comment
from django.contrib.auth import login, logout, authenticate, get_user_model
from .forms import UserRegistrationForm, LoginForm, CommentForm
User = get_user_model()


def home(request):
    my_posts = Post.objects.all()
    context = {"posts": my_posts}
    return render(request, 'blog/home.html', context)


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
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            print(user)
            if user:
                login(request, user)
                return redirect('home')
            else:
                return redirect('register')
        else:
            pass
        context = {'form': form}
    else:
        form = LoginForm()
        context = {'form': form}
    return render(request, 'blog/login.html', context)


def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            user = User.objects.create(username=username, password=password, first_name=first_name, last_name=last_name,
                                       email=email)
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


def logout_view(request):
    logout(request)
    return redirect('login')


def comment_view(request):
    if request.method == "Post":
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            comment = Comment.objects.create(content=content)
            comment.save()
        context = {'comment_form': form}
    else:
        form = CommentForm()
        context = {'comment_form': form}
    return render(request, 'blog/single_post.html', context)
