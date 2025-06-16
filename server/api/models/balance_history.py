import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Double,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, relationship, mapped_column

from server.api.models.models import Base

if TYPE_CHECKING:
    from server.api.models import UserQueries


class BalanceHistory(Base):
    __tablename__ = 'balance_history'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    transaction_type: Mapped[Optional[str]] = mapped_column(String(30))
    amount: Mapped[Optional[float]] = mapped_column(Double(53))
    timestamp: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    query_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('user_queries.query_id', ondelete='CASCADE'),
        nullable=False,
    )

    query: Mapped['UserQueries'] = relationship(
        'UserQueries',
        back_populates='balance_histories',
    )

    def __str__(self):
        return f"История баланса ({self.id})"