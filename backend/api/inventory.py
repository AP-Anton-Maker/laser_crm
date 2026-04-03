from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import List

from ..db.session import get_db
from ..db.models import Inventory
from ..schemas.inventory import InventoryCreate, InventoryUpdate, InventoryResponse

router = APIRouter(prefix="/api/inventory", tags=["Inventory"])


@router.get("/", response_model=List[InventoryResponse])
async def get_all_inventory(db: AsyncSession = Depends(get_db)):
    """
    Получение полного списка всех позиций на складе.
    """
    stmt = select(Inventory).order_by(Inventory.item_name.asc())
    result = await db.execute(stmt)
    items = result.scalars().all()
    return items


@router.get("/low-stock", response_model=List[InventoryResponse])
async def get_low_stock_items(db: AsyncSession = Depends(get_db)):
    """
    Получение списка товаров, у которых количество меньше или равно минимальному порогу.
    Используется для отображения предупреждений на дашборде.
    Формула: quantity <= min_quantity
    """
    stmt = select(Inventory).where(Inventory.quantity <= Inventory.min_quantity)
    result = await db.execute(stmt)
    items = result.scalars().all()
    return items


@router.post("/create", response_model=InventoryResponse, status_code=status.HTTP_201_CREATED)
async def create_inventory_item(
    item_data: InventoryCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Добавление новой позиции на склад.
    """
    new_item = Inventory(**item_data.model_dump())
    
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    
    return new_item


@router.post("/update", response_model=InventoryResponse)
async def update_inventory_item(
    item_data: InventoryUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Обновление параметров существующей позиции на складе.
    Обновляются только переданные поля (quantity, min_quantity и т.д.).
    """
    # Поиск позиции по ID
    item = await db.get(Inventory, item_data.id)
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Позиция склада с ID {item_data.id} не найдена"
        )

    # Подготовка данных для обновления (исключаем None значения)
    update_data = item_data.model_dump(exclude_unset=True, exclude={'id'})
    
    # Поочередное обновление полей
    for field, value in update_data.items():
        if value is not None:
            setattr(item, field, value)
            
    # Дата обновления обновится автоматически благодаря модели (onupdate=datetime.utcnow)
    
    await db.commit()
    await db.refresh(item)
    
    return item
