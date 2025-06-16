from sqlalchemy import (
    ForeignKey,
)
from sqlalchemy.orm import Mapped, relationship, mapped_column

from server.api.models.models import Base


class CountryLanguage(Base):
    __tablename__ = 'country_languages'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    country_id: Mapped[int] = mapped_column(ForeignKey('countries.id'))
    language_id: Mapped[int] = mapped_column(ForeignKey('languages.id'))

    country: Mapped['Countries'] = relationship(back_populates='language_links')
    language: Mapped['Language'] = relationship(back_populates='country_links')
