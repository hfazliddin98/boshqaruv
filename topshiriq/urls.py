from django.urls import path
from users.choices import RoleChoice
from topshiriq.views import topshiriq_home, topshiriq_create, topshiriq_list, topshiriq_update
from topshiriq.views import topshiriq_file_delete, topshiriq_delete_message, topshiriq_delete   



urlpatterns = [
    path('topshiriq_home/', topshiriq_home, name='topshiriq_home'),
    path('topshiriq_list/<str:target_role>/', topshiriq_list, name='topshiriq_list'),
    path('topshiriq_create/<str:target_role>/', topshiriq_create, name='topshiriq_create'),
    path('topshiriq_update/<str:target_role>/<uuid:pk>/', topshiriq_update, name='topshiriq_update'),


    path('topshiriq_file_delete/<str:target_role>/<uuid:pk>/', topshiriq_file_delete, name='topshiriq_file_delete'),
    path('topshiriq_delete_message/<str:target_role>/<uuid:pk>/', topshiriq_delete_message, name='topshiriq_delete_message'),
    path('topshiriq_delete/<str:target_role>/<uuid:pk>/', topshiriq_delete, name='topshiriq_delete'),
]