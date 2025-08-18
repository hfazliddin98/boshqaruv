from django.contrib import admin
from .models import Topshiriq, TopshiriqFile, TopshiriqJavob, TopshiriqJavobFile, TopshiriqReport, TopshiriqReportFile


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


class TopshiriqReportFileInline(admin.TabularInline):
    model = TopshiriqReportFile
    extra = 1


@admin.register(TopshiriqReport)
class TopshiriqReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'topshiriq', 'yaratuvchi', 'bajaruvchi', 'status', 'completed_at']
    list_filter = ['status', 'completed_at', 'yaratuvchi__role', 'bajaruvchi__role']
    search_fields = ['topshiriq__title', 'yaratuvchi__username', 'bajaruvchi__username', 'javob']
    date_hierarchy = 'completed_at'
    inlines = [TopshiriqReportFileInline]
    readonly_fields = ['completed_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'topshiriq', 'yaratuvchi', 'bajaruvchi'
        )


@admin.register(TopshiriqReportFile)
class TopshiriqReportFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'report', 'file', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['report__topshiriq__title', 'file']