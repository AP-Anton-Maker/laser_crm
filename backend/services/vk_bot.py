import os
import logging
from typing import Optional
from vkbottle import Bot
from vkbottle.tools import Message
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from ..db.models import ChatMessage
from ..db.session import async_session_maker

# Настройка логгера
logger = logging.getLogger("vk_bot")

VK_TOKEN = os.getenv("VK_TOKEN", "")

bot: Optional[Bot] = None

if VK_TOKEN:
    bot = Bot(token=VK_TOKEN)

    @bot.on.message()
    async def handle_message(message: Message):
        """
        Обработчик входящих сообщений от пользователей ВК.
        Сохраняет сообщение в БД и отправляет автоответ.
        """
        if not message.text:
            return

        vk_user_id = message.from_id
        
        # Создаем новую сессию для фонового процесса бота
        async with async_session_maker() as session:
            try:
                new_msg = ChatMessage(
                    vk_id=vk_user_id,
                    is_admin=False,
                    message_text=message.text,
                    timestamp=datetime.utcnow()
                )
                session.add(new_msg)
                await session.commit()
                logger.info(f"Сообщение от VK:{vk_user_id} сохранено в БД.")

                # Автоответ клиенту
                await message.answer(
                    "Ваше сообщение принято! 🛠\nМастер скоро ответит вам в этом чате."
                )
                
            except Exception as e:
                await session.rollback()
                logger.error(f"Ошибка БД при сохранении сообщения ВК: {e}", exc_info=True)
else:
    logger.warning("VK_TOKEN не найден. Бот ВКонтакте не будет запущен.")
