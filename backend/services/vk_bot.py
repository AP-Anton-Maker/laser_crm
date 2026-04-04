import os
import logging
from vkbottle import Bot
from vkbottle.tools import Message
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from ..db.models import ChatMessage
from ..db.session import async_session_maker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("vk_bot")

VK_TOKEN = os.getenv("VK_TOKEN", "")

bot = None

if VK_TOKEN:
    bot = Bot(token=VK_TOKEN)

    @bot.on.message()
    async def handle_message(message: Message):
        if not message.text:
            return

        vk_user_id = message.from_id
        
        # Создаем новую сессию специально для этого события бота
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
                logger.info(f"Сообщение от VK:{vk_user_id} сохранено.")

                # Автоответ
                await message.answer("Ваше сообщение принято! 🛠 Мастер скоро ответит.")
                
            except Exception as e:
                await session.rollback()
                logger.error(f"Ошибка БД в боте: {e}")
else:
    logger.warning("VK_TOKEN не найден. Бот не активирован.")
