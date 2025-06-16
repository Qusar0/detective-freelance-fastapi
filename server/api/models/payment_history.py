import datetime
import decimal
from typing import Optional

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    Text,
)
from sqlalchemy.orm import Mapped, relationship, mapped_column

from server.api.models.models import Base


class PaymentHistory(Base):
    __tablename__ = 'payment_history'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    transaction_id: Mapped[Optional[int]] = mapped_column(Integer)
    currency: Mapped[Optional[str]] = mapped_column(Text)
    payment_amount: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    operation_type: Mapped[Optional[str]] = mapped_column(Text)
    invoice_id: Mapped[Optional[int]] = mapped_column(Integer)
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('users.id'),
        nullable=False,
    )
    email: Mapped[Optional[str]] = mapped_column(Text)
    date_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    ip_address: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[Optional[str]] = mapped_column(Text)

    user: Mapped['UserQueries'] = relationship(
        'Users',
        back_populates='payment_histories',
    )

    def __str__(self):
        return f"История пополнения ({self.id})"
