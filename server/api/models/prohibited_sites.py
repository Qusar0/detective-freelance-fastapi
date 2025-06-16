from typing import Optional

from sqlalchemy import (
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from server.api.models.models import Base


class ProhibitedSites(Base):
    __tablename__ = 'prohibited_sites'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    site_link: Mapped[Optional[str]] = mapped_column(String(100))

    def __str__(self):
        return f"Запрещенный сайт ({self.site_link})"
