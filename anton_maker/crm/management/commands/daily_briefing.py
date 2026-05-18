from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from crm.models import Order, SystemLog
from crm.utils.notifications import send_vk_notification
from django.conf import settings

class Command(BaseCommand):
    help = 'Отправляет ежедневную сводку по заказам администратору'

    def handle(self, *args, **options):
        yesterday = timezone.now().date() - timedelta(days=1)
        orders_count = Order.objects.filter(created_at__date=yesterday).count()
        done_count = Order.objects.filter(completed_at__date=yesterday, status='DONE').count()
        
        message = f"📊 Ежедневная сводка за {yesterday.strftime('%d.%m.%Y')}:\n"
        message += f"Новых заказов: {orders_count}\n"
        message += f"Выполнено: {done_count}"
        
        admin_id = getattr(settings, 'VK_ADMIN_ID', None)
        if admin_id:
            send_vk_notification(admin_id, message)
            self.stdout.write(self.style.SUCCESS('Сводка отправлена'))
        else:
            self.stdout.write(self.style.WARNING('VK_ADMIN_ID не настроен'))
