from django.contrib import admin
from django.urls import path
from app1.views import home_page, about_page, product_page, login_form, login_view, logout_view, add_to_cart, remove_from_cart, cart_page, fines_page, complaints_page

urlpatterns = [
    path('', home_page, name='home'),
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('registration/', login_form, name='registration'),
    path('logout/', logout_view, name='logout'),
    path('home/', home_page, name='home'),
    path('about/', about_page, name='about'),
    path('cart/', cart_page, name='cart'),
    path('cart/add/<int:id>', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:id>', remove_from_cart, name='remove_from_cart'),
    path('product/<int:id>', product_page, name='product'),
    path('fines/', fines_page, name='fines'),
    path('complaints/', complaints_page, name='complaints'),
]

