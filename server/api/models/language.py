from typing import List, TYPE_CHECKING

from sqlalchemy import (
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, relationship, mapped_column

from server.api.models.models import Base

if TYPE_CHECKING:
    from server.api.models import CountryLanguage


class Language(Base):
    __tablename__ = 'languages'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    english_name: Mapped[str] = mapped_column(String(100), nullable=False)
    russian_name: Mapped[str] = mapped_column(String(100), nullable=False)

    country_links: Mapped[List['CountryLanguage']] = relationship(
        back_populates='language',
        cascade='all, delete-orphan'
    )
