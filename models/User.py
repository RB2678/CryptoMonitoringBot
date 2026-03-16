from typing import TYPE_CHECKING
from sqlalchemy import BigInteger, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base

if TYPE_CHECKING:
    from models.Alert import Alert

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str | None] = mapped_column(String(32))
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    alerts: Mapped[list["Alert"]] = relationship("Alert", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User(telegram_id={self.telegram_id}, username={self.username})>'