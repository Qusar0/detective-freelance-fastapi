from typing import Optional, TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    Double,
    Integer,
)
from sqlalchemy.orm import Mapped, relationship, mapped_column

from server.api.models.models import Base

if TYPE_CHECKING:
    from server.api.models import Users


class UserBalances(Base):
    __tablename__ = 'user_balances'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    balance: Mapped[Optional[float]] = mapped_column(Double(53))

    user: Mapped['Users'] = relationship(
        'Users',
        back_populates='user_balance',
    )

    def __str__(self):
        return f"Баланс пользователя ({self.id})"
