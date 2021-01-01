import json

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.views.generic.edit import FormMixin
from django.views.generic.list import MultipleObjectMixin

from .forms import UserRegistrationForm, LoginForm
from .models import Post, Comment, CommentLike, Category

User = get_user_model()


class Home(LoginRequiredMixin, ListView):
    model = Category
    ordering = ['slug']
    template_name = 'blog/home.html'


class Posts(LoginRequiredMixin, ListView):
    model = Post
    ordering = ['created_at']
    template_name = 'blog/posts.html'


class Categories(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'blog/category.html'


class SinglePost(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blog/single_post.html'


class Login(LoginView):
    authentication_form = LoginForm


class Logout(LogoutView):
    next_page = 'login'


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'blog/register.html'
    success_url = reverse_lazy('login')
    form_class = UserRegistrationForm
    success_message = "Your profile was created successfully"


@csrf_exempt
def like_dislike(request):
    data = json.loads(request.body)
    user = request.user
    comment = Comment.objects.get(id=data['comment_id'])
    status = data['status']
    try:
        if user in comment.comment_likes['users']:
            comment_like = CommentLike.objects.get(comment=comment, user=user)
            comment_like.status = status
            comment_like.save()
            response = {'like_num': comment.like_count, 'dislike_num': comment.dislike_count,
                        "comment_id": comment.id}
            return HttpResponse(json.dumps(response), status=201)
        else:
            CommentLike.objects.create(status=status, user=user, comment=comment)
            response = {'like_num': comment.like_count, 'dislike_num': comment.dislike_count, "comment_id": comment.id}
            return HttpResponse(json.dumps(response), status=201)
    except:
        response = {"error": "error"}
        return HttpResponse(json.dumps(response), status=400)


@csrf_exempt
def comment_view(request):
    data = json.loads(request.body)
    user = request.user
    try:
        comment = Comment.objects.create(post=Post.objects.get(slug=data['post']), content=data['content'], author=user)
        response = {"content": comment.content, "created_at": str(comment.created_at), "author": comment.author.get_full_name(), "comment_id": comment.id, 'like_num': comment.like_count, 'dislike_num': comment.dislike_count}
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
