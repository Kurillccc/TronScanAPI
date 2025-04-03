from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.wallet import WalletRequest
from app.core.database import get_db
from app.schemas.wallet import WalletRequestCreate, WalletRequestResponse
from app.services.tron_client import get_tron_info

router = APIRouter()

@router.post("/wallet", response_model=WalletRequestResponse)
async def create_wallet_request(
    request: WalletRequestCreate, db: AsyncSession = Depends(get_db)
):
    # Запрос к Tron API
    wallet_info = await get_tron_info(request.wallet_address)
    if not wallet_info:
        raise HTTPException(status_code=404, detail="Wallet not found")
    # Сохранение в БД
    db_wallet = WalletRequest(
        wallet_address=request.wallet_address,
        bandwidth=wallet_info['bandwidth'],
        energy=wallet_info['energy'],
        balance=wallet_info['balance'],
    )
    db.add(db_wallet)
    await db.commit()
    await db.refresh(db_wallet)
    return db_wallet
