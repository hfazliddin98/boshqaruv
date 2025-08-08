from django.urls import path
from users.views import home, kirish
from rektor.views import rektor_home
from rektor.views import prorektor_list, prorektor_create, prorektor_update

from rektor.views import (
    topshiriq_list, topshiriq_create, topshiriq_update, 
    topshiriq_file_delete, topshiriq_delete_message, topshiriq_delete,
)



urlpatterns = [
    path('rektor_home/', rektor_home, name='rektor_home'),

    # Prorektorlar
    path('prorektor_list/', prorektor_list, name='prorektor_list'),
    path('prorektor_create/', prorektor_create, name='prorektor_create'),
    path('prorektor_update/<str:pk>/', prorektor_update, name='prorektor_update'),

    # topshiriq
    path('topshiriq_list/', topshiriq_list, name='topshiriq_list'),
    path('topshiriq_create/', topshiriq_create, name='topshiriq_create'),
    path('topshiriq_update/<str:pk>/', topshiriq_update, name='topshiriq_update'),
    path('topshiriq_file_delete/<str:pk>/', topshiriq_file_delete, name='topshiriq_file_delete'),
    path('topshiriq_delete_message/<str:pk>/', topshiriq_delete_message, name='topshiriq_delete_message'),
    path('topshiriq_delete/<str:pk>/', topshiriq_delete, name='topshiriq_delete'),
]