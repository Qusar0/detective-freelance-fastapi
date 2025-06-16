from typing import List

from sqlalchemy import (
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, relationship, mapped_column

from server.api.models.models import Base


class Countries(Base):
    __tablename__ = 'countries'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    country_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    language_links: Mapped[List['CountryLanguage']] = relationship(
        back_populates='country',
        cascade='all, delete-orphan'
    )
