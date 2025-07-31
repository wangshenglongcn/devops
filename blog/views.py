from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from .models import Posts
from .forms import PostForm, RegisterForm


def post_list(request):
    posts = Posts.objects.all()[:5]
    return render(request, "blog/post_list.html", {"posts": posts})


def post_detail(request, id):
    post = get_object_or_404(Posts, id=id)
    return render(request, "blog/post_detail.html", {"post": post})


def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.pushlish_date = timezone.now()
            post.save()
            return redirect("post_detail", id=post.id)
    else:
        form = PostForm()

    return render(request, "blog/post_create.html", {"form": form})


def post_delete(request, id):
    storage = messages.get_messages(request)
    storage.used = True

    # 只有超级用户或者博客所属用户可以删除对应文章
    post = get_object_or_404(Posts, id=id)
    if not request.user.is_superuser and request.user != post.author:
        messages.error(request, "你无权删除")
        return redirect("post_detail", id=id)

    post.delete()
    messages.success(request, "文章已删除")
    return redirect("post_list")


def register(request):
    storage = messages.get_messages(request)
    storage.used = True
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 注册后自动登录
            return redirect("post_list")  # 跳转到首页或其他页面
        else:
            messages.error(request, "注册信息错误")
    else:
        form = RegisterForm()
    return render(request, "blog/register.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("post_list")


def user_login(request):
    storage = messages.get_messages(request)
    storage.used = True
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # 登录用户
            return redirect("post_list")
        else:
            messages.error(request, "用户名或密码错误")

    return render(request, "blog/login.html")
