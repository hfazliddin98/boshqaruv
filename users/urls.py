from django.urls import path
from users.views import home, kirish, chiqish
from users.views import user_list, user_create, user_update
from users.views import admin_foydalanuvchi_list, admin_foydalanuvchi_create, admin_foydalanuvchi_update
from users.views import admin_struktura_list, admin_struktura_create, admin_struktura_update




urlpatterns = [
    path('', home, name='home'),
    path('kirish/', kirish, name='kirish'),
    path('chiqish/', chiqish, name='chiqish'),

    # users
    path('user_list/<str:target_role>/', user_list, name='user_list'),
    path('user_create/<str:target_role>/', user_create, name='user_create'),
    path('user_update/<str:target_role>/<str:pk>/', user_update, name='user_update'),

    # admin
    path('admin_foydalanuvchi_list/<str:target_role>/', admin_foydalanuvchi_list, name='admin_foydalanuvchi_list'),
    path('admin_foydalanuvchi_create/<str:target_role>/', admin_foydalanuvchi_create, name='admin_foydalanuvchi_create'),
    path('admin_foydalanuvchi_update/<str:target_role>/<uuid:pk>/', admin_foydalanuvchi_update, name='admin_foydalanuvchi_update'),

    # admin struktura
    path('admin_struktura_list/<str:target_role>/', admin_struktura_list, name='admin_struktura_list'),
    path('admin_struktura_create/<str:target_role>/', admin_struktura_create, name='admin_struktura_create'),
    path('admin_struktura_update/<str:target_role>/<uuid:pk>/', admin_struktura_update, name='admin_struktura_update'),

]