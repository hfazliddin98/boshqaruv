from django.urls import path
from users.views import home, kirish
from users.views import admin_home, bolim_boshligi_home, hodim_home
from users.views import prorektor_home, prorektor_bolim_rahbarlar


urlpatterns = [
    path('', home, name='home'),
    path('kirish/', kirish, name='kirish'),

    # users
    path('admin_home/', admin_home, name='admin_home'),
    path('bolim_boshligi_home/', bolim_boshligi_home, name='bolim_boshligi_home'),
    path('hodim_home/', hodim_home, name='hodim_home'),

    # prorektor
    path('prorektor_home/', prorektor_home, name='prorektor_home'),
    path('prorektor_bolim_rahbarlar/', prorektor_bolim_rahbarlar, name='prorektor_bolim_rahbarlar'),

]