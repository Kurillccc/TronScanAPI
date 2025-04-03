from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.api.endpoints.wallet import router as wallet_router
from app.api.endpoints.history import router as history_router
from app.core.database import get_db
from app.models.wallet import WalletRequest
from app.services.tron_client import get_tron_info
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select
from contextlib import asynccontextmanager

app = FastAPI(
    title="Tron Wallet Info API",
    description="API для получения информации о кошельках и их истории запросов в сети Tron.",
    version="1.0.0"
)

# Добавляем эндпоинты
app.include_router(wallet_router, prefix="/api/v1", tags=["Wallet"])
app.include_router(history_router, prefix="/api/v1", tags=["History"])

# Настройка подключения к базе данных
DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"

# Создаем асинхронный движок
engine = create_async_engine(DATABASE_URL, echo=True)

# Создаем сессию
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@app.get("/")
async def read_root():
    return {"message": "API working!"}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Стартап
    async with engine.begin() as conn:
        await conn.run_sync(declarative_base().metadata.create_all)
    print("База данных подключена и таблицы созданы!")
    yield
    # Шатдаун
    await engine.dispose()
    print("Соединение с базой данных закрыто!")


@app.post("/api/v1/wallet")
async def create_wallet_request(wallet_address: str, db: AsyncSession = Depends(get_db)):
    """
    Эндпоинт для запроса информации о кошельке в сети Tron.
    Записывает информацию в базу данных.
    """
    # Получаем данные из сети Tron
    tron_info = await get_tron_info(wallet_address)

    if not tron_info:
        raise HTTPException(status_code=404, detail="Информация о кошельке не найдена")

    # Записываем данные в базу данных
    wallet_request = WalletRequest(
        wallet_address=wallet_address,
        bandwidth=tron_info['bandwidth'],
        energy=tron_info['energy'],
        balance=tron_info['balance']
    )
    db.add(wallet_request)
    await db.commit()  # Асинхронный commit

    return {"message": "Запрос выполнен успешно", "wallet_address": wallet_address}


@app.get("/api/v1/history")
async def get_wallet_history(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    """
    Эндпоинт для получения истории запросов кошельков с пагинацией.
    """
    # Получаем записи с пагинацией
    query = select(WalletRequest).order_by(WalletRequest.timestamp.desc()).offset(skip).limit(limit)
    result = await db.execute(query)

    wallet_requests = result.scalars().all()  # Получаем все строки как объекты

    if not wallet_requests:
        raise HTTPException(status_code=404, detail="Записи не найдены")

    return {"history": wallet_requests}
