from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/dbname"

    class Config:
        # Чтение переменных окружения из файла .env
        env_file = ".env"

# Создание экземпляра настроек
settings = Settings()

# Создание асинхронного движка для подключения к БД
engine = create_async_engine(settings.DATABASE_URL, future=True, echo=True)

# Создание сессии для взаимодействия с БД
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# Функция для получения сессии базы данных
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
