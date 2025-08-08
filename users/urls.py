from django.urls import path
from users.views import home, kirish, chiqish
# from users.views import rektor_home, rektor_prorektorlar, rektor_prorektor_update, rektor_prorektor_create
# from users.views import prorektor_home
# from users.views import prorektor_bolim_boshliqlar, prorektor_bolim_boshliq_create, prorektor_bolim_boshliq_update
# from users.views import prorektor_dekanlar, prorektor_dekan_create, prorektor_dekan_update
# from users.views import admin_home, bolim_boshligi_home, hodim_home


urlpatterns = [
    path('', home, name='home'),
    path('kirish/', kirish, name='kirish'),
    path('chiqish/', chiqish, name='chiqish'),

    # users
    # path('admin_home/', admin_home, name='admin_home'),
    # path('bolim_boshligi_home/', bolim_boshligi_home, name='bolim_boshligi_home'),
    # path('hodim_home/', hodim_home, name='hodim_home'),

    # # rektor
    # path('rektor_home/', rektor_home, name='rektor_home'),
    # path('rektor_prorektorlar/', rektor_prorektorlar, name='rektor_prorektorlar'),
    # path('rektor_prorektor_create/', rektor_prorektor_create, name='rektor_prorektor_create'),
    # path('rektor_prorektor_update/<str:pk>/', rektor_prorektor_update, name='rektor_prorektor_update'),

    # # prorektor
    # path('prorektor_home/', prorektor_home, name='prorektor_home'),
    # path('prorektor_bolim_boshliqlar/', prorektor_bolim_boshliqlar, name='prorektor_bolim_boshliqlar'),
    # path('prorektor_bolim_boshliq_create/', prorektor_bolim_boshliq_create, name='prorektor_bolim_boshliq_create'),
    # path('prorektor_bolim_boshliq_update/<str:pk>/', prorektor_bolim_boshliq_update, name='prorektor_bolim_boshliq_update'),
    # path('prorektor_dekanlar/', prorektor_dekanlar, name='prorektor_dekanlar'),
    # path('prorektor_dekan_create/', prorektor_dekan_create, name='prorektor_dekan_create'),
    # path('prorektor_dekan_update/<str:pk>/', prorektor_dekan_update, name='prorektor_dekan_update'),

]