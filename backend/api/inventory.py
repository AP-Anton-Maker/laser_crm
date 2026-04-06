from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.session import get_db
from db.models import Inventory, User
from schemas import InventoryCreate, InventoryUpdate, InventoryResponse
from api.deps import get_current_active_user

router = APIRouter(prefix="/inventory", tags=["Склад"])

@router.post("/", response_model=InventoryResponse, status_code=status.HTTP_201_CREATED)
async def create_inventory_item(
    item_in: InventoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Добавляет новый материал/товар на склад."""
    stmt = select(Inventory).where(Inventory.name == item_in.name)
    result = await db.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Товар с таким названием уже существует.")

    new_item = Inventory(**item_in.model_dump())
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item

@router.get("/", response_model=List[InventoryResponse])
async def read_inventory(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Получает весь список склада.
    Фронтенд сможет выделить позиции, у которых quantity < min_quantity_alert.
    """
    stmt = select(Inventory).order_by(Inventory.name)
    result = await db.execute(stmt)
    return result.scalars().all()

@router.put("/{item_id}", response_model=InventoryResponse)
async def update_inventory_item(
    item_id: int,
    item_in: InventoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Обновляет количество или лимиты товара."""
    item = await db.get(Inventory, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Товар не найден")

    update_data = item_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)

    await db.commit()
    await db.refresh(item)
    return item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_inventory_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Удаляет позицию со склада."""
    item = await db.get(Inventory, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Товар не найден")
        
    await db.delete(item)
    await db.commit()
