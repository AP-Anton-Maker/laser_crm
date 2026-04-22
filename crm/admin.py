from django.contrib import admin
from unfold.admin import ModelAdmin  # <-- Магия красивого интерфейса!
from .models import Client, Material, Order, QuickReply

@admin.register(Client)
class ClientAdmin(ModelAdmin):
    # Что показываем в таблице
    list_display = ('full_name', 'vk_id', 'phone', 'total_spent', 'cashback_balance')
    # По каким полям работает строка поиска
    search_fields = ('full_name', 'vk_id', 'phone')
    # Поля, которые нельзя редактировать руками (заполняются автоматически)
    readonly_fields = ('created_at',)

@admin.register(Material)
class MaterialAdmin(ModelAdmin):
    list_display = ('name', 'price_per_meter', 'in_stock')
    # Позволяет менять наличие на складе и цену прямо из таблицы, не заходя внутрь!
    list_editable = ('price_per_meter', 'in_stock')
    search_fields = ('name',)

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ('id', 'client', 'status', 'final_price', 'is_paid', 'created_at')
    # Боковая панель фильтров (удобно искать "только неоплаченные" или "в работе")
    list_filter = ('status', 'is_paid', 'material', 'created_at')
    search_fields = ('id', 'client__full_name', 'client__vk_id')
    # Быстрое переключение статусов прямо из списка
    list_editable = ('status', 'is_paid')
    readonly_fields = ('created_at',)

    # Красивая группировка полей внутри карточки заказа
    fieldsets = (
        ('Основная информация', {
            'fields': ('client', 'status')
        }),
        ('Техническое задание (ТЗ)', {
            'fields': ('description', 'material', 'cut_length'),
            'classes': ('tab',) # Unfold позволяет делать табы (вкладки)
        }),
        ('Файлы от клиента', {
            'fields': ('layout_file', 'receipt_image')
        }),
        ('Финансы', {
            'fields': ('final_price', 'is_paid')
        }),
        ('Служебное', {
            'fields': ('admin_notes', 'created_at'),
            'classes': ('collapse',) # Сворачиваемый блок для экономии места
        }),
    )

@admin.register(QuickReply)
class QuickReplyAdmin(ModelAdmin):
    list_display = ('title',)
    search_fields = ('title', 'message_text')
