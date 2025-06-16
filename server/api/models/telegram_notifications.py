from typing import Optional

from sqlalchemy import (
    ForeignKey,
    Integer,
)
from sqlalchemy.orm import Mapped, relationship, mapped_column

from server.api.models.models import Base


class TelegramNotifications(Base):
    __tablename__ = 'telegram_notifications'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    chat_id: Mapped[Optional[int]] = mapped_column(Integer, unique=True)

    user: Mapped['UserQueries'] = relationship(
        'Users',
        back_populates='telegram_notification',
    )

    def __str__(self):
        return f"Телеграм уведомления ({self.id})"
