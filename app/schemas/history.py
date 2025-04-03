from pydantic import BaseModel
from typing import List, Optional

# Схема для ответа с историей запросов
class WalletRequestHistoryResponse(BaseModel):
    id: int
    wallet_address: str
    timestamp: str  # Время запроса в виде строки
    bandwidth: Optional[int] = None
    energy: Optional[int] = None
    balance: Optional[int] = None

    class Config:
        orm_mode = True

# Схема для получения списка запросов (пагинация)
class WalletRequestListResponse(BaseModel):
    total_count: int
    wallets: List[WalletRequestHistoryResponse]

    class Config:
        orm_mode = True
