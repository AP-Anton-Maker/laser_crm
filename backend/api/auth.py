from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.session import get_db
from db.models import User, UserRole
from schemas import Token, UserResponse
from core.security import verify_password, get_password_hash, create_access_token
from api.deps import get_current_active_user

router = APIRouter(prefix="/auth", tags=["Авторизация"])

async def create_default_admin(db: AsyncSession) -> None:
    """
    Создает суперпользователя admin/admin при запуске системы,
    если в базе данных еще нет ни одного администратора.
    """
    stmt = select(User).where(User.username == "admin")
    result = await db.execute(stmt)
    admin_user = result.scalar_one_or_none()

    if not admin_user:
        hashed_pw = get_password_hash("admin")
        new_admin = User(
            username="admin",
            hashed_password=hashed_pw,
            role=UserRole.admin,
            is_active=True
        )
        db.add(new_admin)
        await db.commit()

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    Эндпоинт для авторизации. Принимает username и password из формы,
    проверяет хэш пароля и возвращает JWT токен.
    """
    stmt = select(User).where(User.username == form_data.username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь заблокирован"
        )

    # Генерация токена
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: User = Depends(get_current_active_user)
):
    """
    Возвращает информацию о текущем авторизованном пользователе.
    """
    return current_user
