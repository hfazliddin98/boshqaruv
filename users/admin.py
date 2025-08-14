from django.contrib import admin
from users.models import Users, Struktura


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'last_name', 'first_name', 'role', 'is_active']


@admin.register(Struktura)
class StrukturaAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'birlik_turi', 'role']


