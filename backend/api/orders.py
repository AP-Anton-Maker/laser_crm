# Импорты моделей и схем
import json
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from typing import List, Optional
from ..db.session import get_db
from ..db.models import Order, Client, CashbackHistory
from datetime import datetime
from ..schemas.order import OrderCreate, OrderStatusUpdate, OrderResponse
from ..services.calculator import SmartCalculator

# Создаем роутеры
router = APIRouter(prefix="/api/orders", tags=["Orders"])
action_router = APIRouter(prefix="/api/order", tags=["Order Actions"])


@router.get("/", response_model=List[OrderResponse])
async def get_orders(
    status: Optional[str] = Query(None, description="Фильтр по статусу (NEW, PROCESSING и т.д.)"),
    db: AsyncSession = Depends(get_db)
):
    """
    Получение списка всех заказов.
    Опционально можно фильтровать по статусу через query параметр ?status=NEW
    """
    # Формируем базовый запрос с подгрузкой связанного клиента (чтобы получить имя)
    stmt = select(Order).options(selectinload(Order.client))
    
    if status:
        # Приводим статус к верхнему регистру для единообразия, если нужно
        stmt = stmt.where(Order.status == status.upper())
    
    # Добавляем сортировку по дате создания (новые сверху)
    stmt = stmt.order_by(Order.created_at.desc())
    
    result = await db.execute(stmt)
    orders = result.scalars().all()
    
    # Формируем ответ, добавляя имя клиента вручную, так как в модели ответа оно отдельным полем
    response_list = []
    for order in orders:
        # Конвертируем параметры из JSON строки обратно в словарь для ответа
        order_data = OrderResponse.model_validate(order)
        if order.client:
            order_data.client_name = order.client.name
        # Преобразуем строку параметров обратно в dict для фронтенда
        try:
            if order.parameters:
                order_data.parameters = json.loads(order.parameters)
        except (json.JSONDecodeError, TypeError):
            order_data.parameters = {}
            
        response_list.append(order_data)
        
    return response_list


@action_router.post("/status", response_model=OrderResponse)
async def update_order_status(
    status_ OrderStatusUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Обновление статуса заказа с автоматическим начислением кэшбэка и обновлением статистики клиента,
    если заказ переводится в статус 'DONE'.
    """
    # 1. Находим заказ
    order = await db.get(Order, status_data.order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")

    old_status = order.status
    new_status = status_data.status.upper()
    
    # 2. Обновляем статус
    order.status = new_status
    order.updated_at = datetime.utcnow()

    # 3. БИЗНЕС-ЛОГИКА: Если заказ завершен (DONE)
    if new_status == "DONE" and old_status != "DONE":
        client = await db.get(Client, order.client_id)
        if client:
            # --- Обновление статистики LTV ---
            client.total_orders += 1
            client.total_spent += order.total_price
            
            # --- Начисление кэшбэка (5%) ---
            cashback_amount = order.total_price * 0.05
            client.cashback_balance += cashback_amount
            client.cashback_earned_total += cashback_amount
            
            # --- Запись в историю кэшбэка ---
            history_entry = CashbackHistory(
                client_id=client.id,
                order_id=order.id,
                operation_type="earned",
                amount=cashback_amount,
                description=f"Начислено за заказ #{order.id}"
            )
            db.add(history_entry)
            
            # --- Автоматическая сегментация ---
            if client.total_spent > 50000:
                client.customer_segment = "vip"
            elif client.total_spent > 15000:
                client.customer_segment = "loyal"
            elif client.total_spent > 5000:
                client.customer_segment = "regular"
            # else остается 'new' или текущий, если меньше 5000

    # Коммитим все изменения (статус заказа + данные клиента + история кэшбэка)
    await db.commit()
    
    # Обновляем объект заказа для ответа
    await db.refresh(order)
    await db.refresh(order, attribute_names=['client'])
    
    response_data = OrderResponse.model_validate(order)
    if order.client:
        response_data.client_name = order.client.name
        
    try:
        response_data.parameters = json.loads(order.parameters)
    except:
        response_data.parameters = {}
        
    return response_data
