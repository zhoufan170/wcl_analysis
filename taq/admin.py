from django.contrib import admin
from taq.models import ViscidusPoisonTick

# Register your models here.


class ViscidusPoisonTickAdmin(admin.ModelAdmin):
    search_fields = ('name', 'damage')
    list_display = ('name', 'damage', 'hit', 'tick', 'uptime') + admin.ModelAdmin.list_display


admin.site.register(ViscidusPoisonTick, ViscidusPoisonTickAdmin)