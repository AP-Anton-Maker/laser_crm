from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Dict, Any

from db.session import get_db
from db.models import Order, User
from api.deps import get_current_active_user

router = APIRouter(prefix="/api/analytics", tags=["Аналитика"])

@router.get("/", response_model=Dict[str, Any])
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Сводная статистика: выручка, прибыль, количество заказов."""
    
    # Считаем количество заказов по каждому статусу (новые, в работе, готовы)
    orders_result = await db.execute(select(Order.status, func.count(Order.id)).group_by(Order.status))
    orders_by_status = dict(orders_result.all())
    total_orders = sum(orders_by_status.values())
    
    # Считаем общую выручку (только с готовых/выданных заказов)
    revenue_result = await db.execute(
        select(func.sum(Order.price)).where(Order.status.in_(["ready", "delivered"]))
    )
    total_revenue = revenue_result.scalar() or 0.0
    
    # Считаем чистую прибыль (выручка минус себестоимость)
    profit_result = await db.execute(
        select(func.sum(Order.price - Order.cost_price)).where(Order.status.in_(["ready", "delivered"]))
    )
    total_profit = profit_result.scalar() or 0.0
    
    return {
        "total_orders": total_orders,
        "orders_by_status": orders_by_status,
        "total_revenue": total_revenue,
        "total_profit": total_profit
    }
