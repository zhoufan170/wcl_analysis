from django.contrib import admin
from taq.models import ViscidusPoisonTick, BossNatureProtection

# Register your models here.


class ViscidusPoisonTickAdmin(admin.ModelAdmin):
    search_fields = ('name', 'damage')
    list_display = ('name', 'damage', 'hit', 'tick', 'uptime') + admin.ModelAdmin.list_display


class BossNatureProtectionAdmin(admin.ModelAdmin):
    search_fields = ('enemy__name', 'friendly__name')
    list_display = ('name', 'importance', 'nature_protection_absorb', 'nature_protection_cast', 'major_nature_protection_absorb', 'major_nature_protection_cast') + admin.ModelAdmin.list_display


admin.site.register(ViscidusPoisonTick, ViscidusPoisonTickAdmin)
admin.site.register(BossNatureProtection, BossNatureProtectionAdmin)