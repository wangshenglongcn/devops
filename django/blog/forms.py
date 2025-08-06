from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Posts


class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "请输入标题"}
            ),
            "content": forms.Textarea(
                attrs={"class": "form-control", "rows": 5, "placeholder": "请输入内容"}
            ),
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label="邮箱",
        required=False,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "请输入邮箱，可选"}
        ),
    )

    password1 = forms.CharField(
        label="密码",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "请输入密码"}
        ),
    )
    password2 = forms.CharField(
        label="确认密码",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "请再次输入密码"}
        ),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "请输入用户名"}
            ),
        }
