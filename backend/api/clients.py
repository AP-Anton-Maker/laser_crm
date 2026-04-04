from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from ..db.session import get_db
from ..db.models import Client, CashbackHistory
from ..schemas.all_schemas import ClientResponse, CashbackHistoryResponse
from .auth import get_current_user
from ..db.models import User

router = APIRouter(prefix="/api", tags=["Clients"])

@router.get("/clients", response_model=List[ClientResponse])
async def get_clients(segment: str = Query(None), db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    stmt = select(Client)
    if segment:
        stmt = stmt.where(Client.segment == segment)
    stmt = stmt.order_by(Client.total_spent.desc())
    result = await db.execute(stmt)
    return result.scalars().all()

@router.get("/cashback/history/{client_id}", response_model=List[CashbackHistoryResponse])
async def get_cashback_history(client_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    stmt = select(CashbackHistory).where(CashbackHistory.client_id == client_id).order_by(CashbackHistory.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()
