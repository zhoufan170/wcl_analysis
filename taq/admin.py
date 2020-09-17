from django.contrib import admin
from taq.models import ViscidusPoisonTick, BossNatureProtection, TaqGoldRunDetail

# Register your models here.


class ViscidusPoisonTickAdmin(admin.ModelAdmin):
    search_fields = ('name', 'damage')
    list_display = ('name', 'damage', 'hit', 'tick', 'uptime') + admin.ModelAdmin.list_display


class BossNatureProtectionAdmin(admin.ModelAdmin):
    search_fields = ('enemy__name', 'friendly__name')
    list_display = ('name', 'importance', 'nature_protection_absorb', 'nature_protection_cast', 'major_nature_protection_absorb', 'major_nature_protection_cast') + admin.ModelAdmin.list_display


class TaqGoldRunDetailAdmin(admin.ModelAdmin):
    search_fields = ('name', 'log__name')
    list_display = ('name', 'tag', 'classic', 'base_gold', 'total_gold', 'titan', 'tank', 'heal_total', 'heal_classic', 'heal_boss', 'dispel', 'dps_total_melee', 'dps_total_range', 'dps_punishment', 'dps_boss', 'dps_qiraji_champion', 'dps_qiraji_slayer', 'dps_qiraji_mindslayer', 'dps_obsidian_nullifier', 'jumper', 'other_punishment') + admin.ModelAdmin.list_display


admin.site.register(ViscidusPoisonTick, ViscidusPoisonTickAdmin)
admin.site.register(BossNatureProtection, BossNatureProtectionAdmin)
admin.site.register(TaqGoldRunDetail, TaqGoldRunDetailAdmin)