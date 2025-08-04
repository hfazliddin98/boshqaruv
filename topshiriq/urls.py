from django.urls import path
from users.views import home, kirish
from topshiriq.views import rektor_topshiriq, rektor_topshiriq_create, rektor_topshiriq_update, rektor_topshiriq_file_delete
from topshiriq.views import rektor_topshiriq_delete_message, rektor_topshiriq_delete
from topshiriq.views import prorektor_topshiriq, prorektor_topshiriq_create, prorektor_topshiriq_update


urlpatterns = [

    # rektor
    path('rektor_topshiriq/', rektor_topshiriq, name='rektor_topshiriq'),
    path('rektor_topshiriq_create/', rektor_topshiriq_create, name='rektor_topshiriq_create'),
    path('rektor_topshiriq_update/<str:pk>/', rektor_topshiriq_update, name='rektor_topshiriq_update'),
    path('rektor_topshiriq_file_delete/<str:pk>/', rektor_topshiriq_file_delete, name='rektor_topshiriq_file_delete'),
    path('rektor_topshiriq_delete_message/<str:pk>/', rektor_topshiriq_delete_message, name='rektor_topshiriq_delete_message'),
    path('rektor_topshiriq_delete/<str:pk>/', rektor_topshiriq_delete, name='rektor_topshiriq_delete'),

    # prorektor
    path('prorektor_topshiriq/', prorektor_topshiriq, name='prorektor_topshiriq'),
    path('prorektor_topshiriq_create/', prorektor_topshiriq_create, name='prorektor_topshiriq_create'),
    path('prorektor_topshiriq_update/<str:pk>/', prorektor_topshiriq_update, name='prorektor_topshiriq_update'),

]