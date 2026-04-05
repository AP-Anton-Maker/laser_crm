import logging
from vkbottle import Bot
from vkbottle.bot import Message
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.config import settings
from db.session import async_session_maker
from db.models import Client, ChatMessage

logger = logging.getLogger("vk_bot")

# Инициализируем бота только если в конфиге есть токен
bot = Bot(token=settings.vk_token) if settings.vk_token else None

if bot:
    @bot.on.message()
    async def message_handler(message: Message):
        """Обработка всех входящих сообщений из ВК."""
        async with async_session_maker() as session:
            # 1. Ищем клиента в базе по его VK ID
            result = await session.execute(select(Client).where(Client.vk_id == str(message.from_id)))
            client = result.scalars().first()
            
            # 2. Если клиента нет, создаем его автоматически
            if not client:
                try:
                    # Запрашиваем имя и фамилию у API ВК
                    users_info = await bot.api.users.get(user_ids=[message.from_id])
                    user_name = f"{users_info[0].first_name} {users_info[0].last_name}" if users_info else f"VK Пользователь {message.from_id}"
                except Exception:
                    user_name = f"VK Пользователь {message.from_id}"
                
                client = Client(name=user_name, vk_id=str(message.from_id))
                session.add(client)
                await session.flush() # Получаем ID клиента до коммита
            
            # 3. Сохраняем сообщение в базу
            new_msg = ChatMessage(
                client_id=client.id,
                direction="in",
                text=message.text,
                is_read=False
            )
            session.add(new_msg)
            await session.commit()
            logger.info(f"Получено и сохранено сообщение от VK ID: {message.from_id}")
