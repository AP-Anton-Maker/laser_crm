from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from db.session import get_db
from db.models import Client, User
from schemas import ClientCreate, ClientResponse
from api.deps import get_current_active_user

router = APIRouter(prefix="/api/clients", tags=["Клиенты"])

@router.post("/", response_model=ClientResponse)
async def create_client(
    client_in: ClientCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Добавление нового клиента в базу."""
    if client_in.vk_id:
        result = await db.execute(select(Client).where(Client.vk_id == client_in.vk_id))
        existing_client = result.scalars().first()
        if existing_client:
            raise HTTPException(status_code=400, detail="Клиент с таким VK ID уже существует")
            
    new_client = Client(**client_in.model_dump())
    db.add(new_client)
    await db.commit()
    await db.refresh(new_client)
    return new_client

@router.get("/", response_model=List[ClientResponse])
async def get_clients(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Получение полного списка всех клиентов."""
    result = await db.execute(select(Client))
    return result.scalars().all()

@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(
    client_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Получение информации о конкретном клиенте."""
    result = await db.execute(select(Client).where(Client.id == client_id))
    client = result.scalars().first()
    if not client:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return client

@router.delete("/{client_id}")
async def delete_client(
    client_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Удаление клиента из базы."""
    result = await db.execute(select(Client).where(Client.id == client_id))
    client = result.scalars().first()
    if not client:
        raise HTTPException(status_code=404, detail="Клиент не найден")
        
    await db.delete(client)
    await db.commit()
    return {"message": "Клиент успешно удален"}
