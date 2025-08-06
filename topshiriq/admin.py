from django.contrib import admin
from .models import (
    RektorTopshiriq, RektorTopshiriqFile, RektorTopshiriqJavob, RektorTopshiriqJavobFile,
    ProrektorBolimTopshiriq, ProrektorBolimTopshiriqFile, ProrektorBolimTopshiriqJavob, ProrektorBolimTopshiriqJavobFile,
    ProrektorDekanTopshiriq, ProrektorDekanTopshiriqFile, ProrektorDekanTopshiriqJavob, ProrektorDekanTopshiriqJavobFile
)


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

@admin.register(RektorTopshiriqJavob)
class RektorTopshiriqJavobAdmin(admin.ModelAdmin):
    list_display = ('id', 'rektor_topshiriq', 'bajaruvchi_user', 'title')
    search_fields = ('title', 'rektor_topshiriq__title', 'bajaruvchi_user__username')
    list_filter = ('rektor_topshiriq', 'bajaruvchi_user')

@admin.register(RektorTopshiriqJavobFile)
class RektorTopshiriqJavobFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'rektor_topshiriq_javob', 'file')
    search_fields = ('rektor_topshiriq_javob__title', 'file')
    list_filter = ('rektor_topshiriq_javob',)

# Prorektor bo‘lim topshiriqlari
@admin.register(ProrektorBolimTopshiriq)
class ProrektorBolimTopshiriqAdmin(admin.ModelAdmin):
    list_display = ('id', 'yaratuvchi_user', 'bajaruvchi_user', 'title', 'status', 'xolat')
    search_fields = ('title', 'yaratuvchi_user__username', 'bajaruvchi_user__username')
    list_filter = ('status', 'xolat', 'yaratuvchi_user', 'bajaruvchi_user')
    ordering = ('-created_at',)

@admin.register(ProrektorBolimTopshiriqFile)
class ProrektorBolimTopshiriqFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'prorektor_bolim_topshiriq', 'file')
    search_fields = ('prorektor_bolim_topshiriq__title', 'file')
    list_filter = ('prorektor_bolim_topshiriq',)

@admin.register(ProrektorBolimTopshiriqJavob)
class ProrektorBolimTopshiriqJavobAdmin(admin.ModelAdmin):
    list_display = ('id', 'prorektor_bolim_topshiriq', 'bajaruvchi_user', 'title')
    search_fields = ('title', 'prorektor_bolim_topshiriq__title', 'bajaruvchi_user__username')
    list_filter = ('prorektor_bolim_topshiriq', 'bajaruvchi_user')

@admin.register(ProrektorBolimTopshiriqJavobFile)
class ProrektorBolimTopshiriqJavobFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'prorektor_bolim_topshiriq_javob', 'file')
    search_fields = ('prorektor_bolim_topshiriq_javob__title', 'file')
    list_filter = ('prorektor_bolim_topshiriq_javob',)

# Prorektor dekan topshiriqlari
@admin.register(ProrektorDekanTopshiriq)
class ProrektorDekanTopshiriqAdmin(admin.ModelAdmin):
    list_display = ('id', 'yaratuvchi_user', 'bajaruvchi_user', 'title', 'status', 'xolat')
    search_fields = ('title', 'yaratuvchi_user__username', 'bajaruvchi_user__username')
    list_filter = ('status', 'xolat', 'yaratuvchi_user', 'bajaruvchi_user')
    ordering = ('-created_at',)

@admin.register(ProrektorDekanTopshiriqFile)
class ProrektorDekanTopshiriqFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'prorektor_dekan_topshiriq', 'file')
    search_fields = ('prorektor_dekan_topshiriq__title', 'file')
    list_filter = ('prorektor_dekan_topshiriq',)

@admin.register(ProrektorDekanTopshiriqJavob)
class ProrektorDekanTopshiriqJavobAdmin(admin.ModelAdmin):
    list_display = ('id', 'prorektor_dekan_topshiriq', 'bajaruvchi_user', 'title')
    search_fields = ('title', 'prorektor_dekan_topshiriq__title', 'bajaruvchi_user__username')
    list_filter = ('prorektor_dekan_topshiriq', 'bajaruvchi_user')

@admin.register(ProrektorDekanTopshiriqJavobFile)
class ProrektorDekanTopshiriqJavobFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'prorektor_dekan_topshiriq_javob', 'file')
    search_fields = ('prorektor_dekan_topshiriq_javob__title', 'file')
    list_filter = ('prorektor_dekan_topshiriq_javob',)
