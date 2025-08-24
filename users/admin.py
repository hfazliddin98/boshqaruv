from django.contrib import admin
from users.models import Users, Struktura


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['username', 'last_name', 'first_name', 'role', 'is_active', 'is_superuser']


@admin.register(Struktura)
class StrukturaAdmin(admin.ModelAdmin):
    list_display = ['name', 'birlik_turi', 'role']


