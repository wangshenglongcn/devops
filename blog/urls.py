from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('posts/', views.post_list, name='post_list'),              # GET -- list posts, POST -- create new post
    path('posts/<int:pk>/', views.post_detail, name='post_detail')  # GET -- post detail, POST -- edit post, DELETE -- delete post
]