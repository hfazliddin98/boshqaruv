from django.urls import path
from prorektor.views import prorektor_home
from prorektor.views import bolim_rahbar_list, bolim_rahbar_create, bolim_rahbar_update
from prorektor.views import dekan_list, dekan_create, dekan_update
from prorektor.views import bolim_rahbar_topshiriq_list, bolim_rahbar_topshiriq_update, bolim_rahbar_topshiriq_create
from prorektor.views import dekan_topshiriq_list, dekan_topshiriq_create, dekan_topshiriq_update
from prorektor.views import rektor_topshiriq_list


urlpatterns = [
   path('', prorektor_home, name='prorektor_home'),

   path('bolim_rahbar_list/', bolim_rahbar_list, name='bolim_rahbar_list'),
   path('bolim_rahbar_create/', bolim_rahbar_create, name='bolim_rahbar_create'),
   path('bolim_rahbar_update/<str:pk>/', bolim_rahbar_update, name='bolim_rahbar_update'),

   path('dekan_list/', dekan_list, name='dekan_list'),
   path('dekan_create/', dekan_create, name='dekan_create'),
   path('dekan_update/<str:pk>/', dekan_update, name='dekan_update'),

   path('rektor_topshiriq_list/', rektor_topshiriq_list, name='rektor_topshiriq_list'),

   path('bolim_rahbar_topshiriq_list/', bolim_rahbar_topshiriq_list, name='bolim_rahbar_topshiriq_list'),
   path('bolim_rahbar_topshiriq_create/', bolim_rahbar_topshiriq_create, name='bolim_rahbar_topshiriq_create'),
   path('bolim_rahbar_topshiriq_update/<str:pk>/', bolim_rahbar_topshiriq_update, name='bolim_rahbar_topshiriq_update'),

   path('dekan_topshiriq_list/', dekan_topshiriq_list, name='dekan_topshiriq_list'),
   path('dekan_topshiriq_create/', dekan_topshiriq_create, name='dekan_topshiriq_create'),
   path('dekan_topshiriq_update/<str:pk>/', dekan_topshiriq_update, name='dekan_topshiriq_update'),
]