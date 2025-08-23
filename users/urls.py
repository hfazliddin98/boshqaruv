from django.urls import path
from users.views import home, kirish, chiqish
from users.views import user_list, user_create, user_update
from users.views import admin_foydalanuvchi_list, admin_foydalanuvchi_create


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

]