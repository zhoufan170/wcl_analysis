from django.contrib import admin
from api.models import ApiToken


# Register your models here.
class ApiTokenAdmin(admin.ModelAdmin):
    search_fields = ('name', 'token')
    list_display = ('name', 'token') + admin.ModelAdmin.list_display


admin.site.register(ApiToken, ApiTokenAdmin)
