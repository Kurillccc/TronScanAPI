from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, func, BigInteger
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class WalletRequest(Base):
    __tablename__ = "wallet_requests"

    id: int = Column(Integer, primary_key=True, index=True)
    wallet_address: str = Column(String, nullable=False)
    timestamp: DateTime = Column(DateTime, default=func.now())

    bandwidth: Optional[int] = Column(BigInteger, nullable=True)
    energy: Optional[int] = Column(BigInteger, nullable=True)
    balance: Optional[int] = Column(BigInteger, nullable=True)

    def __repr__(self) -> str:
        return f"<WalletRequest(id={self.id}, wallet_address={self.wallet_address}, timestamp={self.timestamp})>"
