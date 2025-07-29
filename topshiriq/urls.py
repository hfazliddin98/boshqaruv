from django.urls import path
from users.views import home, kirish
from topshiriq.views import rektor_toposhiriq, rektor_toposhiriq_create, rektor_toposhiriq_update
from topshiriq.views import prorektor_toposhiriq, prorektor_toposhiriq_create, prorektor_toposhiriq_update


urlpatterns = [

    # rektor
    path('rektor_toposhiriq/', rektor_toposhiriq, name='rektor_toposhiriq'),
    path('rektor_toposhiriq_create/', rektor_toposhiriq_create, name='rektor_toposhiriq_create'),
    path('rektor_toposhiriq_update/<int:pk>/', rektor_toposhiriq_update, name='rektor_toposhiriq_update'),

    # prorektor
    path('prorektor_toposhiriq/', prorektor_toposhiriq, name='prorektor_toposhiriq'),
    path('prorektor_toposhiriq_create/', prorektor_toposhiriq_create, name='prorektor_toposhiriq_create'),
    path('prorektor_toposhiriq_update/<int:pk>/', prorektor_toposhiriq_update, name='prorektor_toposhiriq_update'),
]