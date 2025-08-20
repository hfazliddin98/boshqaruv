from django.contrib import admin
from .models import Topshiriq, TopshiriqFile, TopshiriqJavob, TopshiriqJavobFile, TopshiriqReport


class TopshiriqFileInline(admin.TabularInline):
    model = TopshiriqFile
    extra = 0


@admin.register(Topshiriq)
class TopshiriqAdmin(admin.ModelAdmin):
    list_display = ('title', 'yaratuvchi_user', 'bajaruvchi_user', 'status', 'xolat', 'boshlanish_vaqti', 'tugash_vaqti', 'created_at')
    list_filter = ('status', 'xolat', 'yaratuvchi_user__role', 'bajaruvchi_user__role', 'created_at')
    search_fields = ('title', 'body', 'yaratuvchi_user__first_name', 'yaratuvchi_user__last_name', 'bajaruvchi_user__first_name', 'bajaruvchi_user__last_name')
    date_hierarchy = 'created_at'
    inlines = [TopshiriqFileInline]


class TopshiriqJavobFileInline(admin.TabularInline):
    model = TopshiriqJavobFile
    extra = 0


@admin.register(TopshiriqJavob)
class TopshiriqJavobAdmin(admin.ModelAdmin):
    list_display = ('title', 'topshiriq', 'bajaruvchi_user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'body', 'topshiriq__title', 'bajaruvchi_user__first_name', 'bajaruvchi_user__last_name')
    inlines = [TopshiriqJavobFileInline]


@admin.register(TopshiriqFile)
class TopshiriqFileAdmin(admin.ModelAdmin):
    list_display = ('topshiriq', 'file', 'created_at')
    search_fields = ('topshiriq__title', 'file')


@admin.register(TopshiriqJavobFile)
class TopshiriqJavobFileAdmin(admin.ModelAdmin):
    list_display = ('javob', 'file', 'created_at')
    search_fields = ('javob__title', 'file')


@admin.register(TopshiriqReport)
class TopshiriqReportAdmin(admin.ModelAdmin):
    list_display = ('topshiriq', 'title', 'status', 'priority', 'yaratuvchi', 'bajaruvchi', 'created_at')
    list_filter = ('status', 'priority', 'is_archived', 'created_at')
    search_fields = ('title', 'topshiriq__title', 'yaratuvchi__first_name', 'yaratuvchi__last_name', 'bajaruvchi__first_name', 'bajaruvchi__last_name')
    date_hierarchy = 'created_at'
    readonly_fields = ('view_count', 'full_report')
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('topshiriq', 'javob', 'title', 'summary')
        }),
        ('Foydalanuvchilar', {
            'fields': ('yaratuvchi', 'bajaruvchi', 'tasdiqlovchi')
        }),
        ('Holat va boshqarish', {
            'fields': ('status', 'priority', 'rating', 'comment')
        }),
        ('Vaqt ma\'lumotlari', {
            'fields': ('deadline', 'completed_at', 'approved_at', 'rejected_at')
        }),
        ('Qo\'shimcha', {
            'fields': ('view_count', 'is_archived', 'full_report'),
            'classes': ('collapse',)
        })
    )
