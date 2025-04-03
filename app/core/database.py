from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Создание движка базы данных
engine = create_async_engine(settings.DATABASE_URL, future=True, echo=True)

# Создание фабрики сессий
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# Функция для получения сессии БД
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
