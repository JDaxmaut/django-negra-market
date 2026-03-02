from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth import login, logout
from django.db import IntegrityError
import random

from .models import RegistrationForm, LoginForm

# Сатирические описания товаров в средневековом стиле
PRODUCT_DESCRIPTIONS = [
    "Лёгкая броня. Если не попадут — не убьют.",
    "Для тех, кто верит, что лучшая защита — это нападение. Или бегство.",
    "Выковано с молитвой. Работает не всегда.",
    "Серебряная насечка для солидности. Не ржавеет (почти).",
    "Проверено в бою. Владелец не выжил, но броня цела.",
    "Идеально для парадов. В бою блестит и отвлекает врага.",
    "Надёжная как стена. Тяжёлая как стена.",
    "Для рыцарей с ипотекой — дешевле гробов.",
    "Руны защиты включены. Батарейки не прилагаются.",
    "Специальная цена для вдов павших воинов.",
    "Не пробивается стрелами. Магией — возможно.",
    "В комплекте: пот, слёзы и немного крови.",
    "Гарантия 30 дней или возврат трупа.",
    "Выбор чемпионов. Большинство погибло в расцвете лет.",
    "Лёгкая как перо. Защита как у пера.",
    "Для тех, кто хочет умереть красиво.",
    "Сталь высшего качества. Враг оценит.",
    "Подходит для дуэлей, свадеб и похорон.",
    "Не требует заточки. Заточит себя сама.",
    "Острый как правда. Редко врёт.",
    "Клинок прошёл тесты. Тесты не прошли.",
    "Для левой и правой руки. И для ног тоже.",
    "Сбалансирован идеально. В обе стороны.",
    "Можно резать, колоть, метать. Или продать.",
    "В рукояти скрытый отсек для яда (пустой).",
    "Любимое оружие палачей и поэтов.",
    "Не ржавеет от крови. Только от воды.",
    "Гравировка 'Смерть врагам' включена.",
    "Подходит для вскрытия доспехов и консервов.",
    "Если не справится — у нас есть копья.",
]

# Отзывы покупателей
REVIEWS = [
    ("Сэр Родрик", 5, "Пережил 3 битвы. Жена довольна — вернулся."),
    ("Чёрный Рыцарь", 1, "Проржавел после первого дождя. 0/10"),
    ("Ланселот Младший", 4, "Хороший меч. Рукоять маловата."),
    ("Вдова Маргарет", 5, "Муж погиб, но красиво. Спасибо!"),
    ("Гарет Дракон", 3, "Нормально, но шлем жмёт уши."),
    ("Сэр Падший", 2, "Не защищает от магии. Верните деньги."),
    ("Тристан", 5, "Лучший щит! Враг сломал меч, не щит."),
    ("Мерлин", 1, "Слишком много железа. Магии нет."),
    ("Ивейн", 4, "Качество хорошее. Доставка долгая."),
    ("Персиваль", 5, "Идеально для крестового похода!"),
    ("Борс", 3, "Средне. За эти деньги ожидал большего."),
    ("Агравейн", 2, "Шлем протекает. Не рекомендую."),
    ("Томас", 5, "Дёшево и сердито. Враг мёртв."),
    ("Оливер", 4, "Хороший баланс. Рука не устаёт."),
    ("Годфри", 1, "Сломался о первый доспех. Позор!"),
    ("Рейнальд", 5, "Кровь отмывается легко. 5 звёзд."),
    ("Хью", 3, "Нормально для новичка."),
    ("Вальтер", 4, "Тяжёлый, но надёжный."),
    ("Эдмунд", 2, "Не подошёл по размеру. Возврат?"),
    ("Жанна", 5, "Лучшее в гильдии! Рекомендую!"),
]


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
    # Генерируем описание и отзывы для товара
    random.seed(id)  # Чтобы у одного товара всегда было одно описание
    description = random.choice(PRODUCT_DESCRIPTIONS)
    
    # Выбираем 2-3 случайных отзыва для этого товара
    num_reviews = random.randint(2, 3)
    reviews = random.sample(REVIEWS, num_reviews)
    
    data = {
        "id": id,
        "description": description,
        "reviews": reviews,
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



