from django.conf import settings
from crm.bot_logic.vk_client import VKClient
from crm.models import SystemLog

vk_bot = VKClient()

def send_vk_notification(user_id, message):
    try:
        vk_bot.send_message(user_id, message)
        return True
    except Exception as e:
        SystemLog.objects.create(level='ERROR', message=f"VK notification failed: {str(e)}")
        return False

def notify_admin_about_order(order):
    admin_id = getattr(settings, 'VK_ADMIN_ID', None)
    if admin_id:
        message = f"🔔 Новый заказ #{order.id}\nКлиент: {order.client.full_name}\nСумма: {order.final_price}₽"
        send_vk_notification(admin_id, message)
