from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from crm.models import Material, QuickReply

@admin.register(Material)
class MaterialAdmin(ModelAdmin):
    list_display = ('name', 'price_per_unit', 'in_stock', 'min_stock_level', 'is_active', 'stock_alert')
    list_filter = ('is_active',)
    search_fields = ('name',)
    
    def stock_alert(self, obj):
        if obj.in_stock <= obj.min_stock_level:
            return format_html('<span style="color: red; font-weight: bold;">⚠️ Мало!</span>')
        return format_html('<span style="color: green;">✓ OK</span>')
    stock_alert.short_description = "Статус"

@admin.register(QuickReply)
class QuickReplyAdmin(ModelAdmin):
    list_display = ('title',)
    search_fields = ('title', 'text')
