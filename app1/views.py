from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth import login, logout
from django.db import IntegrityError

from .models import RegistrationForm, LoginForm

# Create your views here.
def home_page(request):
    name = 'Alex'
    languages = ['Python', 'Java Script']
    data = {"name": name, "languages": languages}
    return render(request, "home_page.html", context=data)

def about_page(request):
    company_name = "The Great IT GigaCompany"
    date_of_founded = "02.05.1998"
    description = "Ведущая IT-компания, \
        которая создает инновационные цифровые решения для бизнеса по всему миру. \
        Мы разрабатываем мощные веб- и мобильные приложения, внедряем искусственный интеллект и обеспечиваем надежную облачную инфраструктуру. \
        В фокусе на масштабируемость и передовые технологии, мы помогаем компаниям расти в эпоху цифровизации."
    
    data = {"company_name": company_name, "date_of_founded": date_of_founded, "description": description}
    return render(request, "about.html", context=data)

def goods_page(request):
    return render(request, "goods.html", {"item_count": range(1,6)})

def product_page(request, id):
    data = {
        "id": id
    }
    return render(request, "product.html", context=data)

def login_form(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                return redirect("home")
            except IntegrityError:
                form.add_error("username", "Пользователь с таким именем уже существует")
    else:
        form = RegistrationForm()
    return render(request, "registration.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")



