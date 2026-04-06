import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Laser CRM Enterprise"
    # По умолчанию используем асинхронный драйвер SQLite
    DATABASE_URL: str = "sqlite+aiosqlite:///./laser_crm.sqlite3"
    
    # JWT Настройки
    SECRET_KEY: str = "super_secret_key_laser_crm_2024_enterprise_secure"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 дней
    
    # VK Bot Настройки
    VK_TOKEN: str = "your_vk_group_token_here"
    
    # Бизнес-логика
    MIN_ORDER_PRICE: float = 500.0

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
