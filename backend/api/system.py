from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import List

from db.session import get_db
from db.models import SystemSettings, User
from api.deps import get_current_active_user

router = APIRouter(prefix="/api/system", tags=["Системные настройки"])

class SettingItem(BaseModel):
    key: str
    value: str

@router.get("/settings", response_model=List[SettingItem])
async def get_settings(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Получение всех настроек."""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Доступ разрешен только администраторам")
        
    result = await db.execute(select(SystemSettings))
    return [{"key": s.key, "value": s.value} for s in result.scalars().all()]

@router.post("/settings")
async def update_setting(
    setting: SettingItem,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Обновление или создание новой настройки (например, токена ВК)."""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Доступ разрешен только администраторам")
        
    result = await db.execute(select(SystemSettings).where(SystemSettings.key == setting.key))
    db_setting = result.scalars().first()
    
    if db_setting:
        db_setting.value = setting.value
    else:
        db_setting = SystemSettings(key=setting.key, value=setting.value)
        db.add(db_setting)
        
    await db.commit()
    return {"message": f"Настройка '{setting.key}' успешно сохранена"}
