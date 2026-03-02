from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from app1.views import home_page, about_page, goods_page, product_page, login_form, login_view, logout_view

product_patterns = [
    path("", goods_page, name="goods"),
    path("product/<int:id>", product_page, name="product"),
]

urlpatterns = [
    path('', home_page, name='home'),
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('registration/', login_form, name='registration'),
    path('logout/', logout_view, name='logout'),
    path('home/', home_page, name='home'),
    path('about/', about_page, name='about'),
    path('goods/', include(product_patterns))
]

