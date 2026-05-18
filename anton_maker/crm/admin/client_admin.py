from django.contrib import admin
from unfold.admin import ModelAdmin
from crm.models import Client

@admin.register(Client)
class ClientAdmin(ModelAdmin):
    list_display = ('full_name', 'vk_id', 'phone', 'bot_state', 'notify_enabled', 'created_at')
    search_fields = ('full_name', 'vk_id', 'phone')
    list_filter = ('bot_state', 'notify_enabled')
    readonly_fields = ('vk_id', 'created_at')
    fieldsets = (
        (None, {'fields': ('vk_id', 'full_name', 'phone')}),
        ("Настройки бота", {'fields': ('bot_state', 'notify_enabled')}),
    )
