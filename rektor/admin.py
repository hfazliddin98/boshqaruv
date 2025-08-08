from django.contrib import admin
from rektor.models import RektorTopshiriq, RektorTopshiriqFile, RektorTopshiriqJavob, RektorTopshiriqJavobFile

@admin.register(RektorTopshiriq)
class RektorTopshiriqAdmin(admin.ModelAdmin):  
    list_display = ('id', 'title', 'created_at', 'updated_at')
    search_fields = ('title',)
    list_filter = ('created_at', 'updated_at')

@admin.register(RektorTopshiriqJavob)
class RektorTopshiriqJavobAdmin(admin.ModelAdmin):
    list_display = ('id', 'rektor_topshiriq', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
