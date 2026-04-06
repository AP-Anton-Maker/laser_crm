import logging
from vkbottle.bot import Bot, Message
from sqlalchemy.future import select

from core.config import settings
from db.session import async_session_maker
from db.models import Client, ChatMessage, ChatDirection

logger = logging.getLogger(__name__)

# Инициализируем бота только если токен задан (чтобы локально без ВК не падало приложение)
if settings.VK_TOKEN and settings.VK_TOKEN != "your_vk_group_token_here":
    bot = Bot(token=settings.VK_TOKEN)
else:
    bot = None
    logger.warning("VK_TOKEN не настроен. Бот не будет получать сообщения.")

if bot:
    @bot.on.message()
    async def message_handler(message: Message):
        """
        Перехватывает входящие сообщения из ВК, ищет клиента в БД,
        создает его если нет, и сохраняет сообщение.
        """
        vk_id = message.from_id
        text = message.text

        async with async_session_maker() as db:
            # 1. Ищем клиента по VK ID
            stmt = select(Client).where(Client.vk_id == vk_id)
            result = await db.execute(stmt)
            client = result.scalar_one_or_none()

            # 2. Если клиента нет, получаем его данные из ВК и создаем
            if not client:
                users_info = await bot.api.users.get(user_ids=[vk_id])
                if users_info:
                    first_name = users_info[0].first_name
                    last_name = users_info[0].last_name
                    client_name = f"{first_name} {last_name}"
                else:
                    client_name = f"VK Client {vk_id}"

                client = Client(name=client_name, vk_id=vk_id)
                db.add(client)
                await db.commit()
                await db.refresh(client)

            # 3. Сохраняем входящее сообщение в историю
            chat_msg = ChatMessage(
                client_id=client.id,
                direction=ChatDirection.IN,
                text=text,
                is_read=False
            )
            db.add(chat_msg)
            await db.commit()
            
            logger.info(f"Сохранено сообщение от {client.name}: {text}")
