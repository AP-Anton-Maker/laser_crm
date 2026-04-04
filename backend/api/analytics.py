from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from calendar import monthrange
from datetime import datetime
from typing import List, Dict, Any

from ..db.session import get_db
from ..db.models import Order, Client, User
from ..services.ai_forecast import predict_revenue
from .auth import get_current_user

router = APIRouter(prefix="/api", tags=["Analytics"])

@router.get("/analytics/summary")
async def get_summary(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    stmt = select(func.sum(Order.total_price), func.count(Order.id)).where(Order.status.in_(["DONE", "COMPLETED"]))
    res = await db.execute(stmt)
    row = res.first()
    rev = row[0] or 0.0
    cnt = row[1] or 0
    
    stmt_cb = select(func.sum(Client.cashback_balance)).where(Client.cashback_balance > 0)
    cb_res = await db.execute(stmt_cb)
    cb_total = cb_res.scalar() or 0.0
    
    stmt_top = select(Client.name, Client.total_spent).order_by(Client.total_spent.desc()).limit(5)
    top_res = await db.execute(stmt_top)
    top = [{"name": r.name, "spent": r.total_spent} for r in top_res.all()]
    
    return {
        "revenue": round(rev, 2),
        "orders": cnt,
        "avg_check": round(rev/cnt, 2) if cnt else 0,
        "cashback_debt": round(cb_total, 2),
        "top_clients": top
    }

@router.get("/analytics/services")
async def get_services(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    stmt = select(Order.service_name, func.sum(Order.total_price)).where(Order.status.in_(["DONE", "COMPLETED"])).group_by(Order.service_name)
    res = await db.execute(stmt)
    return [{"name": r.service_name, "value": r[1]} for r in res.all()]

@router.get("/analytics/segments")
async def get_segments(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    stmt = select(Client.segment, func.count(Client.id)).group_by(Client.segment)
    res = await db.execute(stmt)
    return [{"name": r.segment, "value": r[1]} for r in res.all()]

@router.get("/calendar")
async def get_calendar(month: int, year: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    start = datetime(year, month, 1)
    last_day = monthrange(year, month)[1]
    end = datetime(year, month, last_day, 23, 59, 59)
    
    stmt = select(Order).options(selectinload(Order.client)).where(Order.planned_date >= start, Order.planned_date <= end)
    res = await db.execute(stmt)
    orders = res.scalars().all()
    
    data = {}
    for o in orders:
        if not o.planned_date: continue
        key = o.planned_date.strftime("%Y-%m-%d")
        if key not in data: data[key] = []
        data[key].append({
            "id": o.id, "client": o.client.name if o.client else "Unknown", 
            "service": o.service_name, "price": o.total_price, "status": o.status
        })
    return data

@router.get("/ai/predictions")
async def get_predictions(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    pred = await predict_revenue(db)
    return pred if pred else {"prediction": 0, "trend": "stable", "confidence": 0}
