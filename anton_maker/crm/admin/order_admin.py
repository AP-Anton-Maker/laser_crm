from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from unfold.admin import ModelAdmin
from crm.models import Order
from datetime import datetime

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ('id', 'client', 'status', 'material', 'final_price', 'created_at', 'print_ticket_btn')
    list_filter = ('status', 'material', 'created_at')
    search_fields = ('client__full_name', 'description', 'id')
    readonly_fields = ('created_at', 'completed_at')
    
    fieldsets = (
        (None, {'fields': ('client', 'status', 'description')}),
        ("Детали", {'fields': ('material', 'layout_file')}),
        ("Финансы", {'fields': ('estimated_price', 'final_price')}),
        ("Даты", {'fields': ('created_at', 'completed_at')}),
    )

    actions = ['mark_done']

    def mark_done(self, request, queryset):
        queryset.update(status='DONE', completed_at=datetime.now())
    mark_done.short_description = "Отметить как выполненные"

    def print_ticket_btn(self, obj):
        url = reverse('order_ticket', args=[obj.pk])
        return format_html('<a href="{}" target="_blank" class="button">Печать ТЗ</a>', url)
    print_ticket_btn.short_description = "Действия"
