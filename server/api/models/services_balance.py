import decimal
from typing import Optional

from sqlalchemy import (
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from server.api.models.models import Base


class ServicesBalance(Base):
    __tablename__ = 'services_balance'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    service_name: Mapped[Optional[str]] = mapped_column(String)
    balance: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)
    balance_threshold: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric)

    def __str__(self):
        return f"Баланс сервиса ({self.id})"
