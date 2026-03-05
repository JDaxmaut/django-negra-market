from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.db import IntegrityError
import random

from .models import RegistrationForm, LoginForm


def get_cart(request):
    return request.session.get('cart', [])

def save_cart(request, cart):
    request.session['cart'] = cart

def home_page(request):
    cart = get_cart(request)
    items = list(range(1, 17))
    data = {"items": items, "cart": cart}
    return render(request, "home_page.html", context=data)

def add_to_cart(request, id):
    cart = get_cart(request)
    if id not in cart:
        cart.append(id)
        save_cart(request, cart)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def remove_from_cart(request, id):
    cart = get_cart(request)
    if id in cart:
        cart.remove(id)
        save_cart(request, cart)
    referer = request.META.get('HTTP_REFERER', 'home')
    if 'cart' in referer:
        return redirect('cart')
    return redirect('home')

def cart_page(request):
    cart = get_cart(request)
    checkout_error = None
    if request.method == "POST":
        checkout_error = "Недостаточно средств на балансе жизни"
    data = {"cart": cart, "checkout_error": checkout_error}
    return render(request, "cart.html", context=data)

def about_page(request):
    description = "Компания «азон» — это уникальное место для тех, кто мечтает почувствовать себя героем антиутопии в режиме 24/7. Мы возвели эксплуатацию в ранг корпоративной культуры и доказали, что человеческое достоинство — это лишь досадная статья расходов."
    advantages = [
        ("Отрицательная мотивация", "У нас самая низкая зарплата на рынке, которая стабильно уменьшается благодаря филигранной системе штрафов (за моргание, дыхание и мысли об отпуске)."),
        ("График «До победного»", "Работа в режиме 24/0 без права на сон и личную жизнь. Мы верим, что семья — это коллеги, которых вы ненавидите."),
        ("Комфортный «офис»", "Подвальные помещения с естественной вентиляцией через щели в дверях и эргономичные стоячие места."),
        ("Карьерный рост", "Возможность пройти путь от «бесправного стажера» до «виноватого специалиста» всего за один бесконечный рабочий день."),
    ]
    loyalty_title = "Система лояльности в «азоне»"
    loyalty_description = "Это когда мы берем в рабство твоих близких, а тебе выдаем углеводы. Представляем программу «Друг за сухарик»:"
    loyalty_items = [
        ("Механика", "Приведи в наш каторжный отдел свежего кандидата с целыми почками и отсутствием чувства собственного достоинства."),
        ("Твой профит", "Как только твой «протеже» отработает первые 18 часов без перерыва, ты получаешь элитный бонус — одну (1) черствую булку (без начинки, зато с запахом надежды)."),
        ("Акция «Оптом дешевле»", "Приведи пятерых друзей и получи половинку сосиски к своей булке! (Сосиска может содержать следы предыдущих сотрудников)."),
    ]
    loyalty_warning = "Важное условие: Если друг решит сбежать или упадет в обморок в первую смену, стоимость булки вычитается из твоей и без того микроскопической зарплаты в тройном размере."
    data = {
        "description": description,
        "advantages": advantages,
        "loyalty_title": loyalty_title,
        "loyalty_description": loyalty_description,
        "loyalty_items": loyalty_items,
        "loyalty_warning": loyalty_warning,
    }
    return render(request, "about.html", context=data)

def fines_page(request):
    salary = 0.01
    
    # Базовые штрафы
    base_fines = [
        ("За дыхание", 50),
        ("За моргание", 100),
        ("За мысли об отпуске", 500),
        ("За опоздание на 0.0001 сек", 200),
        ("За слишком громкую печать", 150),
        ("За недостаточно громкую печать", 150),
        ("За существование", 1000),
    ]
    
    # Генерируем случайный множитель для пользователя (0.8 - 1.2)
    if 'fines_multiplier' not in request.session:
        request.session['fines_multiplier'] = round(random.uniform(0.8, 1.2), 2)
    
    multiplier = request.session['fines_multiplier']
    
    # Применяем множитель к каждому штрафу
    fines = [(name, int(amount * multiplier)) for name, amount in base_fines]
    total_fines = sum(fine[1] for fine in fines)
    
    data = {
        "salary": salary,
        "fines": fines,
        "total_fines": total_fines,
        "debt": total_fines - salary,
    }
    return render(request, "fines.html", context=data)

def complaints_page(request):
    submitted = False
    if request.method == "POST":
        submitted = True
    data = {"submitted": submitted}
    return render(request, "complaints.html", context=data)

def referral_page(request):
    friend_submitted = False
    if request.method == "POST":
        friend_submitted = True
    data = {"friend_submitted": friend_submitted}
    return render(request, "referral.html", context=data)

def product_page(request, id):
    data = {"id": id}
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



