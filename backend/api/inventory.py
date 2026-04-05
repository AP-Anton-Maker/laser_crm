from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from db.session import get_db
from db.models import Inventory, User
from schemas import InventoryCreate, InventoryUpdate, InventoryResponse
from api.deps import get_current_active_user

router = APIRouter(prefix="/api/inventory", tags=["Склад"])

@router.post("/", response_model=InventoryResponse)
async def create_inventory_item(
    item_in: InventoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Добавление новой позиции материала на склад."""
    new_item = Inventory(**item_in.model_dump())
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item

@router.get("/", response_model=List[InventoryResponse])
async def get_inventory(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Получение всех остатков на складе."""
    result = await db.execute(select(Inventory))
    return result.scalars().all()

@router.put("/{item_id}", response_model=InventoryResponse)
async def update_inventory_item(
    item_id: int,
    item_update: InventoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Обновление количества или стоимости материала."""
    result = await db.execute(select(Inventory).where(Inventory.id == item_id))
    item = result.scalars().first()
    if not item:
        raise HTTPException(status_code=404, detail="Материал не найден на складе")
        
    update_data = item_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
        
    await db.commit()
    await db.refresh(item)
    return item

@router.delete("/{item_id}")
async def delete_inventory_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Удаление позиции со склада."""
    result = await db.execute(select(Inventory).where(Inventory.id == item_id))
    item = result.scalars().first()
    if not item:
        raise HTTPException(status_code=404, detail="Материал не найден на складе")
        
    await db.delete(item)
    await db.commit()
    return {"message": "Материал списан со склада"}
