from django.urls import path
from users.views import home, kirish, chiqish
# from users.views import rektor_home, rektor_prorektorlar, rektor_prorektor_update, rektor_prorektor_create
# from users.views import prorektor_home
# from users.views import prorektor_bolim_boshliqlar, prorektor_bolim_boshliq_create, prorektor_bolim_boshliq_update
# from users.views import prorektor_dekanlar, prorektor_dekan_create, prorektor_dekan_update
# from users.views import admin_home, bolim_boshligi_home, hodim_home
from users.views import user_list, user_create, user_update


urlpatterns = [
    path('', home, name='home'),
    path('kirish/', kirish, name='kirish'),
    path('chiqish/', chiqish, name='chiqish'),

    # users
    path('user_list/<str:target_role>/', user_list, name='user_list'),
    path('user_create/<str:target_role>/', user_create, name='user_create'),
    path('user_update/<str:target_role>/<str:pk>/', user_update, name='user_update'),

  
]