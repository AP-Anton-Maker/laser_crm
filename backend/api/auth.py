from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta

from db.session import get_db
from db.models import User
from core.security import verify_password, get_password_hash, create_access_token
from core.config import settings
from schemas import Token, UserResponse
from api.deps import get_current_active_user

router = APIRouter(prefix="/api/auth", tags=["Авторизация"])

async def create_default_admin(db: AsyncSession):
    """Автоматическое создание пользователя admin/admin при первом запуске."""
    result = await db.execute(select(User).where(User.username == "admin"))
    user = result.scalars().first()
    
    if not user:
        hashed_password = get_password_hash("admin")
        new_admin = User(
            username="admin",
            hashed_password=hashed_password,
            is_superuser=True,
            is_active=True
        )
        db.add(new_admin)
        await db.commit()

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """Эндпоинт для входа и получения токена."""
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalars().first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: User = Depends(get_current_active_user)
):
    """Получение информации о текущем авторизованном пользователе."""
    return current_user
