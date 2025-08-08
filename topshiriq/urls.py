from django.urls import path
from users.views import home, kirish
# from topshiriq.views import (
#     rektor_topshiriq, rektor_topshiriq_create, rektor_topshiriq_update, rektor_topshiriq_file_delete,
#     rektor_topshiriq_delete_message, rektor_topshiriq_delete,
#     prorektor_topshiriq, prorektor_topshiriq_create, prorektor_topshiriq_update,
#     prorektor_rektor_topshiriq_list, prorektor_rektor_topshiriq_javob_create, prorektor_rektor_topshiriq_javob_update,
#     prorektor_bolim_topshiriq_list, prorektor_bolim_topshiriq_create, prorektor_bolim_topshiriq_update,
#     prorektor_dekan_topshiriq_list, prorektor_dekan_topshiriq_create, prorektor_dekan_topshiriq_update,
# )


urlpatterns = [
    # # rektor
    # path('rektor_topshiriq/', rektor_topshiriq, name='rektor_topshiriq'),
    # path('rektor_topshiriq_create/', rektor_topshiriq_create, name='rektor_topshiriq_create'),
    # path('rektor_topshiriq_update/<str:pk>/', rektor_topshiriq_update, name='rektor_topshiriq_update'),
    # path('rektor_topshiriq_file_delete/<str:pk>/', rektor_topshiriq_file_delete, name='rektor_topshiriq_file_delete'),
    # path('rektor_topshiriq_delete_message/<str:pk>/', rektor_topshiriq_delete_message, name='rektor_topshiriq_delete_message'),
    # path('rektor_topshiriq_delete/<str:pk>/', rektor_topshiriq_delete, name='rektor_topshiriq_delete'),

    # # prorektor rektor topshiriqlari
    # path('prorektor_rektor_topshiriq_list/', prorektor_rektor_topshiriq_list, name='prorektor_rektor_topshiriq_list'),
    # path('prorektor_rektor_topshiriq_javob_create/<str:pk>/', prorektor_rektor_topshiriq_javob_create, name='prorektor_rektor_topshiriq_javob_create'),
    # path('prorektor_rektor_topshiriq_javob_update/<str:pk>/', prorektor_rektor_topshiriq_javob_update, name='prorektor_rektor_topshiriq_javob_update'),

    # # prorektor bo‘lim topshiriqlari
    # path('prorektor_bolim_topshiriq_list/', prorektor_bolim_topshiriq_list, name='prorektor_bolim_topshiriq_list'),
    # path('prorektor_bolim_topshiriq_create/', prorektor_bolim_topshiriq_create, name='prorektor_bolim_topshiriq_create'),
    # path('prorektor_bolim_topshiriq_update/<str:pk>/', prorektor_bolim_topshiriq_update, name='prorektor_bolim_topshiriq_update'),

    # # prorektor dekan topshiriqlari
    # path('prorektor_dekan_topshiriq_list/', prorektor_dekan_topshiriq_list, name='prorektor_dekan_topshiriq_list'),
    # path('prorektor_dekan_topshiriq_create/', prorektor_dekan_topshiriq_create, name='prorektor_dekan_topshiriq_create'),
    # path('prorektor_dekan_topshiriq_update/<str:pk>/', prorektor_dekan_topshiriq_update, name='prorektor_dekan_topshiriq_update'),

    # # prorektor umumiy topshiriq (agar kerak bo‘lsa)
    # path('prorektor_topshiriq/', prorektor_topshiriq, name='prorektor_topshiriq'),
    # path('prorektor_topshiriq_create/', prorektor_topshiriq_create, name='prorektor_topshiriq_create'),
    # path('prorektor_topshiriq_update/<str:pk>/', prorektor_topshiriq_update, name='prorektor_topshiriq_update'),
]