from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from ..db.session import get_db
from ..db.models import Inventory, User
from ..schemas.all_schemas import InventoryCreate, InventoryUpdate, InventoryResponse
from .auth import get_current_user

router = APIRouter(prefix="/api/inventory", tags=["Inventory"])

@router.get("/", response_model=List[InventoryResponse])
async def get_inventory(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    stmt = select(Inventory).order_by(Inventory.item_name)
    result = await db.execute(stmt)
    return result.scalars().all()

@router.get("/low-stock", response_model=List[InventoryResponse])
async def get_low_stock(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    stmt = select(Inventory).where(Inventory.quantity <= Inventory.min_quantity)
    result = await db.execute(stmt)
    return result.scalars().all()

@router.post("/create", response_model=InventoryResponse, status_code=status.HTTP_201_CREATED)
async def create_item(item_data: InventoryCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_item = Inventory(**item_data.model_dump())
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item

@router.post("/update", response_model=InventoryResponse)
async def update_item(item_data: InventoryUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    item = await db.get(Inventory, item_data.id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    update_data = item_data.model_dump(exclude_unset=True, exclude={'id'})
    for k, v in update_data.items():
        if v is not None:
            setattr(item, k, v)
    
    await db.commit()
    await db.refresh(item)
    return item
