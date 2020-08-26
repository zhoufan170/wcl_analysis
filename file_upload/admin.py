from django.contrib import admin
from file_upload.models import File, PoisonData

# Register your models here.


class FileAdmin(admin.ModelAdmin):
    search_fields = ('wcl_link', 'absolute_file')
    list_display = ('wcl_link', 'absolute_file', 'upload_time') + admin.ModelAdmin.list_display


class PoisonDataAdmin(admin.ModelAdmin):
    search_fields = ('username', 'file')
    list_display = ('file', 'username', 'tick') + admin.ModelAdmin.list_display


admin.site.register(File, FileAdmin)
admin.site.register(PoisonData, PoisonDataAdmin)