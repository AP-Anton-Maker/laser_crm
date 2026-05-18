from django.core.management.base import BaseCommand
from crm.models import Material, SystemLog
from crm.utils.notifications import send_vk_notification
from django.conf import settings

class Command(BaseCommand):
    help = 'Проверяет остатки материалов и уведомляет о низком запасе'

    def handle(self, *args, **options):
        low_stock = Material.objects.filter(in_stock__lte=min_stock_level, is_active=True)
        
        if not low_stock.exists():
            self.stdout.write(self.style.SUCCESS('Все материалы в достаточном количестве'))
            return
        
        message = "⚠️ Внимание! Заканчиваются материалы:\n"
        for material in low_stock:
            message += f"- {material.name}: {material.in_stock} ед. (мин: {material.min_stock_level})\n"
        
        admin_id = getattr(settings, 'VK_ADMIN_ID', None)
        if admin_id:
            send_vk_notification(admin_id, message)
            self.stdout.write(self.style.SUCCESS('Уведомление отправлено'))
        else:
            self.stdout.write(self.style.WARNING('VK_ADMIN_ID не настроен'))
