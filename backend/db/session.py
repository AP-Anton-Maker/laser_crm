from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from core.config import settings

# Создаем асинхронный движок БД
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# Фабрика асинхронных сессий
async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

# Базовый класс для всех моделей SQLAlchemy
Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Зависимость (Dependency) для FastAPI.
    Выдает асинхронную сессию для каждого запроса и безопасно закрывает её после.
    """
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
