from django.urls import path
from users.choices import RoleChoice
from topshiriq.views import topshiriq_create, topshiriq_list, topshiriq_update
from topshiriq.views import topshiriq_file_delete, topshiriq_delete_message, topshiriq_delete  
from topshiriq.views import topshiriq_javob_create, topshiriq_javob_list, topshiriq_bajaruvchi_list
from topshiriq import views



urlpatterns = [
    # Topshiriq CRUD
    path('topshiriq_list/<str:target_role>/', topshiriq_list, name='topshiriq_list'),
    path('topshiriq_create/<str:target_role>/', topshiriq_create, name='topshiriq_create'),
    path('topshiriq_update/<str:target_role>/<uuid:pk>/', topshiriq_update, name='topshiriq_update'),
    path('topshiriq_detail/<str:target_role>/<uuid:pk>/', views.topshiriq_detail, name='topshiriq_detail'),

    # Topshiriq bajaruvchi list
    path('topshiriq_bajaruvchi_list/<str:target_role>/', topshiriq_bajaruvchi_list, name='topshiriq_bajaruvchi_list'),

    # Topshiriq file operations
    path('topshiriq_file_delete/<str:target_role>/<uuid:pk>/', topshiriq_file_delete, name='topshiriq_file_delete'),
    path('topshiriq_delete_message/<str:target_role>/<uuid:pk>/', topshiriq_delete_message, name='topshiriq_delete_message'),
    path('topshiriq_delete/<str:target_role>/<uuid:pk>/', topshiriq_delete, name='topshiriq_delete'),

    # Javob operations
    path('topshiriq_javob_create/<str:target_role>/<uuid:pk>/', topshiriq_javob_create, name='topshiriq_javob_create'),
    path('topshiriq_javob_list/<str:target_role>/', topshiriq_javob_list, name='topshiriq_javob_list'),
    
    # Hisobot operations - target_role olib tashlandi
    path('hisobot_list/', views.hisobot_list, name='hisobot_list'),
    path('hisobot/export/', views.export_all_reports, name='export_all_reports'),
    path('hisobot_detail/<str:target_role>/<uuid:pk>/', views.hisobot_detail, name='hisobot_detail'),
    path('hisobot/approve/<uuid:report_id>/', views.approve_report, name='approve_report'),
    path('hisobot/reject/<uuid:report_id>/', views.reject_report, name='reject_report'),
    path('hisobot/download/<uuid:report_id>/', views.download_report, name='download_report'),
]