from django.urls import path
from .views import home, posts, login_view, register_view, categories, single_post

urlpatterns = [
    path('', home, name='home'),
    path('posts/', posts, name='posts'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('category/<slug:pk>/', categories, name='categories'),
    path('post/<slug:pk>', single_post, name='post')
]
