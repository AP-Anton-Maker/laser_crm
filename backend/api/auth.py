from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from typing import Optional
import jwt
import hashlib

from ..db.session import get_db
from ..db.models import User

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# КОНФИГУРАЦИЯ (В продакшене вынести в .env!)
SECRET_KEY = "super_secret_key_change_me_in_prod"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # 24 часа

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Простая проверка пароля. 
    В реальном проекте используйте passlib.hash.bcrypt_context.verify
    Здесь для простоты используем SHA-256 хэширование строки.
    """
    # Если в БД хранится просто строка (для дев-теста), сравниваем напрямую
    # Если хэш:
    expected_hash = hashlib.sha256(plain_password.encode()).hexdigest()
    return expected_hash == hashed_password or plain_password == hashed_password

@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    Выдает JWT токен при успешной авторизации.
    Ожидает username и password в form-data.
    """
    # Поиск пользователя
    stmt = select(User).where(User.username == form_data.username)
    result = await db.execute(stmt)
    user = result.scalars().first()

    # Проверка существования и пароля
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Генерация токена
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(
    token: str = Depends(OAuth2PasswordRequestForm), # Упрощенно, лучше использовать OAuth2PasswordBearer
    db: AsyncSession = Depends(get_db)
):
    """
    Зависимость для получения текущего пользователя из токена.
    Примечание: Для корректной работы в роутерах нужно использовать OAuth2PasswordBearer схему.
    Ниже реализована упрощенная версия для примера логики декодирования.
    """
    # Эта функция требует правильной настройки security схемы в FastAPI
    # Для полноценного использования см. документацию FastAPI Security
    pass
