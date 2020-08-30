from django.contrib import admin
from base.models import WCLLog, Fight, Friendly, Enemy

# Register your models here.


class WCLLogAdmin(admin.ModelAdmin):
    search_fields = ('title', 'code')
    list_display = ('title', 'code', 'owner', 'zone') + admin.ModelAdmin.list_display


class FightAdmin(admin.ModelAdmin):
    search_fields = ('name', 'fight_id')
    list_display = ('log', 'name', 'fight_id') + admin.ModelAdmin.list_display


class FriendlyAdmin(admin.ModelAdmin):
    search_fields = ('name', 'friendly_id', 'type')
    list_display = ('log', 'name', 'type', 'guid') + admin.ModelAdmin.list_display


class EnemyAdmin(admin.ModelAdmin):
    search_fields = ('name', 'enemy_id', 'type')
    list_display = ('log', 'name', 'type', 'guid') + admin.ModelAdmin.list_display


admin.site.register(WCLLog, WCLLogAdmin)
admin.site.register(Fight, FightAdmin)
admin.site.register(Friendly, FriendlyAdmin)
admin.site.register(Enemy, EnemyAdmin)