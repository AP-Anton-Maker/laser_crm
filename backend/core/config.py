from pydantic_settings import BaseSettings
from pathlib import Path
import os


class Settings(BaseSettings):
    """
    Конфигурация приложения.
    Загружает переменные окружения или использует значения по умолчанию.
    """
    # URL базы данных
    DATABASE_URL: str = "sqlite+aiosqlite:///../data/laser_crm.sqlite3"
    
    # Токен группы ВКонтакте
    VK_TOKEN: str = os.getenv("VK_TOKEN", "")
    
    # Секретный ключ для JWT (в продакшене менять!)
    SECRET_KEY: str = "super-secret-key-change-me-in-prod"
    
    # Алгоритм шифрования JWT
    ALGORITHM: str = "HS256"
    
    # Время жизни токена в минутах (3000 мин ≈ 2 дня)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 3000

    class Config:
        env_file = ".env"
        extra = "ignore"

    @property
    def database_path_resolved(self) -> str:
        """
        Возвращает путь к БД, предварительно создав директорию, если её нет.
        """
        path_str = self.DATABASE_URL.replace("sqlite+aiosqlite:///", "")
        db_path = Path(path_str)
        
        db_dir = db_path.parent
        if not db_dir.exists():
            db_dir.mkdir(parents=True, exist_ok=True)
            
        return self.DATABASE_URL


settings = Settings()
