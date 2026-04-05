from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from db.session import get_db
from db.models import Order, Client, User
from schemas import OrderCreate, OrderUpdate, OrderResponse
from api.deps import get_current_active_user

# Основной роутер для CRUD операций с заказами
router = APIRouter(prefix="/api/orders", tags=["Заказы"])

# Дополнительный роутер для специфичных действий (например, быстрая смена статуса)
action_router = APIRouter(prefix="/api/orders/{order_id}/action", tags=["Действия с заказами"])

@router.post("/", response_model=OrderResponse)
async def create_order(
    order_in: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Создание нового заказа для существующего клиента."""
    result = await db.execute(select(Client).where(Client.id == order_in.client_id))
    client = result.scalars().first()
    if not client:
        raise HTTPException(status_code=404, detail="Указанный клиент не найден")
        
    new_order = Order(**order_in.model_dump())
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    return new_order

@router.get("/", response_model=List[OrderResponse])
async def get_orders(
    status: Optional[str] = Query(None, description="Фильтр по статусу заказа"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Получение списка заказов (с возможностью фильтрации по статусу)."""
    query = select(Order)
    if status:
        query = query.where(Order.status == status)
        
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Получение карточки конкретного заказа."""
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalars().first()
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order

@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(
    order_id: int,
    order_update: OrderUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Обновление данных заказа (описание, цена, дедлайн)."""
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalars().first()
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
        
    update_data = order_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(order, key, value)
        
    await db.commit()
    await db.refresh(order)
    return order

@router.delete("/{order_id}")
async def delete_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Удаление заказа."""
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalars().first()
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
        
    await db.delete(order)
    await db.commit()
    return {"message": "Заказ успешно удален"}

@action_router.post("/status")
async def change_order_status(
    order_id: int,
    new_status: str = Query(..., description="Новый статус заказа"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Быстрое изменение статуса заказа с начислением кэшбэка при завершении."""
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalars().first()
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
        
    old_status = order.status
    order.status = new_status
    
    # СИСТЕМА ЛОЯЛЬНОСТИ: Если заказ перешел в статус "Выдан", начисляем 5% кэшбэка клиенту
    if new_status == "delivered" and old_status != "delivered":
        client_res = await db.execute(select(Client).where(Client.id == order.client_id))
        client = client_res.scalars().first()
        
        if client:
            cashback_amount = order.price * 0.05
            
            # Если у клиента в базе notes пустое, делаем его строкой
            if not client.notes:
                client.notes = f"Баланс кэшбэка: {cashback_amount} руб."
            elif "Баланс кэшбэка:" in client.notes:
                # Обновляем старую сумму (упрощенная логика для старта)
                client.notes += f" | + {cashback_amount} руб. кэшбэк"
            else:
                client.notes += f" | Баланс кэшбэка: {cashback_amount} руб."
                
    await db.commit()
    return {"message": f"Статус заказа изменен на {new_status}"}
