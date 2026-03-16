from typing import TYPE_CHECKING
from sqlalchemy import String, DateTime, Float, Boolean, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base

if TYPE_CHECKING:
    from models.User import User

class Alert(Base):
    __tablename__ = 'alerts'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    coin: Mapped[str] = mapped_column(String(10))
    target_price: Mapped[float] = mapped_column(Float)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    user: Mapped["User"] = relationship("User", back_populates="alerts")