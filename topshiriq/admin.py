from django.contrib import admin
from .models import RektorTopshiriq, RektorTopshiriqFile        


@admin.register(RektorTopshiriq)
class RektorTopshiriqAdmin(admin.ModelAdmin):   
    list_display = ('id', 'yaratuvchi_user', 'bajaruvchi_user', 'title', 'status', 'xolat')
    search_fields = ('title', 'yaratuvchi_user__username', 'bajaruvchi_user__username')
    list_filter = ('status', 'xolat', 'yaratuvchi_user', 'bajaruvchi_user')
    ordering = ('-created_at',)

@admin.register(RektorTopshiriqFile)
class RektorTopshiriqFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'rektor_topshiriq', 'file')
    search_fields = ('rektor_topshiriq__title', 'file')
    list_filter = ('rektor_topshiriq',)
