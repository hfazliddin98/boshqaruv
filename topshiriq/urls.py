from django.urls import path
from users.choices import RoleChoice
from topshiriq.views import topshiriq_create, topshiriq_list, topshiriq_update
from topshiriq.views import topshiriq_file_delete, topshiriq_delete_message, topshiriq_delete  
from topshiriq.views import topshiriq_javob_create, topshiriq_javob_list, topshiriq_bajaruvchi_list, topshiriq_baxolash
from topshiriq import views
from topshiriq.views import komissiya_statistika_list
from topshiriq.notification_views import notifications_list, notification_detail, mark_all_notifications_read, notification_count_ajax



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
    
    # Baholash operations
    path('topshiriq_baxolash/<str:target_role>/<uuid:pk>/', topshiriq_baxolash, name='topshiriq_baxolash'),
    
    # Hisobot operations - target_role olib tashlandi
    path('hisobot_list/', views.hisobot_list, name='hisobot_list'),

    # Komissiya statistikasi
    path('komissiya_statistika_list/<str:target_role>/', komissiya_statistika_list, name='komissiya_statistika_list'),

    # Bildirishnoma URLs
    path('notifications/', notifications_list, name='notifications_list'),
    path('notification/<uuid:pk>/', notification_detail, name='notification_detail'),
    path('notifications/mark-all-read/', mark_all_notifications_read, name='mark_all_notifications_read'),
    path('notifications/count-ajax/', notification_count_ajax, name='notification_count_ajax'),
]