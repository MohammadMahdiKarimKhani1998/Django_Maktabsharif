from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import ModelFormMixin, FormMixin, BaseCreateView, UpdateView

from .models import Post, Comment, Category
from django.contrib.auth import login, logout, authenticate, get_user_model
from .forms import UserRegistrationForm, LoginForm, CommentForm

from django.views.generic import ListView, DetailView, CreateView, FormView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView

import json
User = get_user_model()


class Home(LoginRequiredMixin, ListView):
    model = Post
    ordering = ['created_at']
    template_name = 'blog/home.html'


class Posts(LoginRequiredMixin, ListView):
    model = Post
    ordering = ['created_at']
    template_name = 'blog/posts.html'


class Categories(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/category.html'


class SinglePost(DetailView):
    model = Post
    template_name = 'blog/single_post.html'


class Login(LoginView):
    authentication_form = LoginForm


class Logout(LogoutView):
    next_page = 'login'


class SignUpView(DetailView):
    template_name = 'blog/register.html'
    success_url = reverse_lazy('register')
    form_class = UserRegistrationForm
    success_message = "Your profile was created successfully"


@csrf_exempt
def like(request):
    data = json.loads(request.body)
    if data:
        return HttpResponse(data)


@csrf_exempt
def comment_view(request):
    data = json.loads(request.body)
    user = request.user
    try:
        comment = Comment.objects.create(post=Post.objects.get(slug=data['post']), content=data['content'], author=user)
        response = {"content": comment.content}
        return HttpResponse(json.dumps(response), status=201)
    except:
        response = {"error": "error"}
        return HttpResponse(json.dumps(response), status=400)

# def login_view(request):
#     # if request.user.is_authenticated:
#     #     return redirect('home')
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             print(user)
#             if user:
#                 login(request, user)
#                 return redirect('home')
#             else:
#                 return redirect('register')
#         else:
#             pass
#         context = {'form': form}
#     else:
#         form = LoginForm()
#         context = {'form': form}
#     return render(request, 'blog/login.html', context)


# def logout_view(request):
#     logout(request)
#     return redirect('login')

# def register_view(request):
#     if request.method == "POST":
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             email = form.cleaned_data['email']
#             user = User.objects.create(username=username, password=password, first_name=first_name, last_name=last_name,
#                                        email=email)
#             user.set_password(password)
#             user.save()
#             print('valid')
#         else:
#             print('invalid')
#         context = {'form': form}
#     else:
#         form = UserRegistrationForm()
#         context = {'form': form}
#     return render(request, 'blog/register.html', context)
