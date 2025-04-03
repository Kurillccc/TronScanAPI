from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.wallet import WalletRequest
from app.core.database import get_db
from app.schemas.wallet import WalletRequestResponse
from typing import List

router = APIRouter()

@router.get("/history", response_model=List[WalletRequestResponse])
async def get_wallets(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(WalletRequest).offset(skip).limit(limit))
    wallets = result.scalars().all()
    return wallets
