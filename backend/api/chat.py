from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from datetime import datetime

from ..db.session import get_db
from ..db.models import ChatMessage
from ..schemas.chat import MessageSend, ChatHistoryResponse
from ..services.vk_bot import bot

router = APIRouter(prefix="/api/chat", tags=["Chat VK"])


@router.get("/history", response_model=List[ChatHistoryResponse])
async def get_chat_history(
    vk_id: int = Query(..., description="ID пользователя ВКонтакте"),
    limit: int = Query(100, description="Лимит сообщений"),
    db: AsyncSession = Depends(get_db)
):
    """История переписки с пользователем ВК."""
    stmt = (
        select(ChatMessage)
        .where(ChatMessage.vk_id == vk_id)
        .order_by(ChatMessage.timestamp.asc())
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("/send", response_model=ChatHistoryResponse)
async def send_message_to_vk(msg_data: MessageSend, db: AsyncSession = Depends(get_db)):
    """Отправка сообщения пользователю ВК из CRM."""
    if bot is None:
        raise HTTPException(status_code=503, detail="Сервис ВКонтакте недоступен")

    new_msg = ChatMessage(
        vk_id=msg_data.vk_id,
        is_admin=True,
        message_text=msg_data.message,
        timestamp=datetime.utcnow()
    )
    
    db.add(new_msg)
    await db.commit()
    await db.refresh(new_msg)

    try:
        await bot.api.messages.send(
            peer_id=msg_data.vk_id,
            message=msg_data.message,
            random_id=0
        )
    except Exception as e:
        print(f"Ошибка отправки ВК: {e}")
        
    return new_msg
