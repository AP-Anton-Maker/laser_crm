import os
import logging
from typing import Optional
from vkbottle import Bot
from vkbottle.tools import Message
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from ..db.models import ChatMessage, SystemSettings
from ..db.session import async_session_maker

logger = logging.getLogger("vk_bot")
VK_TOKEN = os.getenv("VK_TOKEN", "")

bot: Optional[Bot] = None

if VK_TOKEN:
    bot = Bot(token=VK_TOKEN)

    @bot.on.message()
    async def handle_message(message: Message):
        if not message.text:
            return

        vk_user_id = message.from_id
        
        async with async_session_maker() as session:
            try:
                # 1. Сохраняем входящее сообщение в историю
                new_msg = ChatMessage(
                    vk_id=vk_user_id,
                    is_admin=False,
                    message_text=message.text,
                    timestamp=datetime.utcnow()
                )
                session.add(new_msg)
                await session.commit()
                logger.info(f"Сообщение от VK:{vk_user_id} сохранено.")

                # 2. Проверяем настройки системы (Режим отпуска)
                stmt = select(SystemSettings).where(SystemSettings.id == 1)
                res = await session.execute(stmt)
                settings = res.scalars().first()

                response_text = ""

                if settings and settings.is_vacation_mode:
                    # Режим отпуска включен
                    if settings.vacation_message:
                        response_text = settings.vacation_message
                        # Добавляем дату, если она есть
                        if settings.vacation_end_date:
                            response_text += f"\n📅 Ожидаемое возвращение: {settings.vacation_end_date}"
                    else:
                        response_text = "Я сейчас в отпуске. Отвечу, как вернусь!"
                    
                    logger.info(f"Отправлен автоответ об отпуске пользователю {vk_user_id}")
                else:
                    # Стандартный режим
                    response_text = "Ваше сообщение принято! 🛠\nМастер скоро ответит вам в этом чате."

                # 3. Отправляем ответ клиенту
                if response_text:
                    await message.answer(response_text)
                
            except Exception as e:
                await session.rollback()
                logger.error(f"Ошибка БД в боте: {e}", exc_info=True)
else:
    logger.warning("VK_TOKEN не найден. Бот не активирован.")
