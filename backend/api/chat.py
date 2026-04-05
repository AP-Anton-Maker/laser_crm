import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from pydantic import BaseModel

from db.session import get_db
from db.models import ChatMessage, Client, User
from schemas import ChatMessageResponse
from api.deps import get_current_active_user
from services.vk_bot import bot

router = APIRouter(prefix="/api/chat", tags=["Чат ВК"])

class SendMessageRequest(BaseModel):
    text: str

@router.get("/{client_id}", response_model=List[ChatMessageResponse])
async def get_chat_history(
    client_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Получение истории переписки с конкретным клиентом."""
    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.client_id == client_id)
        .order_by(ChatMessage.timestamp.asc())
    )
    messages = result.scalars().all()
    
    # Автоматически помечаем прочитанными все входящие сообщения, когда менеджер открывает чат
    for msg in messages:
        if not msg.is_read and msg.direction == "in":
            msg.is_read = True
    await db.commit()
    
    return messages

@router.post("/{client_id}/send")
async def send_message_to_vk(
    client_id: int,
    payload: SendMessageRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Отправка сообщения клиенту в ВК прямо из интерфейса CRM."""
    result = await db.execute(select(Client).where(Client.id == client_id))
    client = result.scalars().first()
    
    if not client or not client.vk_id:
        raise HTTPException(status_code=400, detail="У этого клиента не указан VK ID")

    if not bot:
        raise HTTPException(status_code=500, detail="ВК бот не настроен (отсутствует токен)")
        
    try:
        # Отправляем в ВК
        await bot.api.messages.send(
            user_id=int(client.vk_id),
            message=payload.text,
            random_id=random.randint(1, 2147483647)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка отправки ВК: {str(e)}")

    # Сохраняем в нашу БД
    new_msg = ChatMessage(
        client_id=client.id,
        direction="out",
        text=payload.text,
        is_read=True
    )
    db.add(new_msg)
    await db.commit()
    
    return {"status": "ok", "message": "Сообщение успешно отправлено"}
