from pydantic import BaseModel
from typing import Optional

# Схема для создания запроса о кошельке
class WalletRequestCreate(BaseModel):
    wallet_address: str

    class Config:
        orm_mode = True

# Схема для ответа с данными о кошельке
class WalletRequestResponse(BaseModel):
    id: int
    wallet_address: str
    timestamp: str  # Время запроса в виде строки
    bandwidth: Optional[int] = None
    energy: Optional[int] = None
    balance: Optional[int] = None

    class Config:
        orm_mode = True  # позволяет работать с ORM-объектами как с Pydantic моделями
