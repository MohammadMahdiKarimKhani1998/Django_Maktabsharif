from django.urls import path
from .views import Home, Posts, SignUpView, Categories, SinglePost, Logout, Login, like_dislike, comment_view

urlpatterns = [
    path('home/', Home.as_view(), name='home'),
    path('posts/', Posts.as_view(), name='posts'),
    path('', Login.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='register'),
    path('category/<slug:category>/', Categories.as_view(), name='categories'),
    path('post/<slug:slug>/', SinglePost.as_view(), name='post'),
    path('comment/', comment_view, name='comment'),
    path('like_dislike/', like_dislike, name='like_dislike'),
]
