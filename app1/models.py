from django import forms
from django.db import models
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        label="Имя пользователя",
        max_length=10,
        min_length=5,
        strip=True,
    )
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя", max_length=150)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())
