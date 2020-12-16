from django.urls import path
from .views import home, posts, login_view, register_view, categories, single_post, logout_view, comment_view

urlpatterns = [
    path('home', home, name='home'),
    path('posts/', posts, name='posts'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', register_view, name='register'),
    path('category/<slug:pk>/', categories, name='categories'),
    path('post/<slug:pk>', single_post, name='post')
]
