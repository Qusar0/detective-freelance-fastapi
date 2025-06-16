import datetime
import decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
)
from sqlalchemy.orm import Mapped, relationship, mapped_column

from server.api.models.models import Base

if TYPE_CHECKING:
    from server.api.models import UserQueries


class QueriesBalance(Base):
    __tablename__ = 'queries_balance'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    query_id: Mapped[int] = mapped_column(
        ForeignKey('user_queries.query_id', ondelete='CASCADE'),
        nullable=False,
    )
    balance: Mapped[decimal.Decimal] = mapped_column(Numeric)
    transaction_date: Mapped[datetime.datetime] = mapped_column(DateTime(True))

    query: Mapped['UserQueries'] = relationship(
        'UserQueries',
        back_populates='queries_balances',
    )

    def __str__(self):
        return f"Баланс запроса ({self.id})"
