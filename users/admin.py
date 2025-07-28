from django.contrib import admin
from users.models import Users, Bolim


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'last_name', 'first_name', 'role', 'bolim', 'is_active']

@admin.register(Bolim)
class BolimAdmin(admin.ModelAdmin):
    list_display = ['id']
