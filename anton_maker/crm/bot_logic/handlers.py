from django.conf import settings
from .vk_client import VKClient
from .keyboards import get_main_keyboard, get_cancel_keyboard
from crm.models import Order, SystemLog
from decimal import Decimal

vk_bot = VKClient()

def process_message(client, text, attachments):
    state = client.bot_state
    
    if text.lower() in ['отмена', 'cancel', 'стоп']:
        client.bot_state = 'START'
        client.save()
        vk_bot.send_message(client.vk_id, "Действие отменено. Выберите команду:", keyboard=get_main_keyboard())
        return

    if state == 'START':
        handle_start(client, text)
    elif state == 'WAIT_DESC':
        handle_wait_desc(client, text)
    elif state == 'WAIT_FILE':
        handle_wait_file(client, text, attachments)
    else:
        client.bot_state = 'START'
        client.save()
        vk_bot.send_message(client.vk_id, "Сессия сброшена. Выберите команду:", keyboard=get_main_keyboard())

def handle_start(client, text):
    if text == '📝 Новый заказ':
        client.bot_state = 'WAIT_DESC'
        client.save()
        vk_bot.send_message(client.vk_id, "Опишите ваш заказ (материал, размеры, пожелания):", keyboard=get_cancel_keyboard())
    elif text == '📦 Мои заказы':
        orders = Order.objects.filter(client=client).order_by('-created_at')[:5]
        if not orders:
            vk_bot.send_message(client.vk_id, "У вас пока нет заказов.")
        else:
            msg = "Ваши последние заказы:\n"
            for order in orders:
                msg += f"#{order.id}: {order.get_status_display()} - {order.final_price}₽\n"
            vk_bot.send_message(client.vk_id, msg)
    elif text == 'ℹ️ Помощь':
        vk_bot.send_message(client.vk_id, "Для создания заказа нажмите '📝 Новый заказ' и следуйте инструкциям.")
    else:
        vk_bot.send_message(client.vk_id, "Выберите команду из меню:", keyboard=get_main_keyboard())

def handle_wait_desc(client, text):
    if not text.strip():
        vk_bot.send_message(client.vk_id, "Пожалуйста, введите описание заказа:")
        return

    order = Order.objects.create(
        client=client,
        description=text,
        status='NEW'
    )
    
    client.bot_state = 'WAIT_FILE'
    client.save()
    
    vk_bot.send_message(client.vk_id, f"Заказ #{order.id} принят! Пришлите файл макета (или напишите 'нет файла' если его нет):", keyboard=get_cancel_keyboard())
    
    notify_admin(f"Новый заказ #{order.id} от {client.full_name}\nОписание: {text}")

def handle_wait_file(client, text, attachments):
    orders = Order.objects.filter(client=client, status='NEW').order_by('-created_at')
    if not orders:
        client.bot_state = 'START'
        client.save()
        vk_bot.send_message(client.vk_id, "Активный заказ не найден. Начните заново.", keyboard=get_main_keyboard())
        return
    
    order = orders.first()
    
    file_url = None
    for att in attachments:
        if att['type'] == 'doc':
            doc = att['doc']
            file_url = doc.get('url')
            filename = f"order_{order.id}_{doc['title']}"
            saved_path = vk_bot.download_file(file_url, filename)
            if saved_path:
                order.layout_file = saved_path
                break
    
    order.save()
    client.bot_state = 'START'
    client.save()
    
    vk_bot.send_message(client.vk_id, f"Заказ #{order.id} успешно оформлен! Мы свяжемся с вами для уточнения деталей.", keyboard=get_main_keyboard())
    notify_admin(f"Файл для заказа #{order.id} загружен: {order.layout_file or 'Нет файла'}")

def notify_admin(message):
    admin_id = getattr(settings, 'VK_ADMIN_ID', None)
    if admin_id:
        try:
            vk_bot.send_message(admin_id, f"🔔 {message}")
        except Exception as e:
            SystemLog.objects.create(level='ERROR', message=f"Failed to notify admin: {str(e)}")
