import logging
from typing import Dict, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError

from server.api.dao.base import BaseDAO
from server.api.models.models import CountryLanguage, Language


class CountryLanguageDAO(BaseDAO):
    model = CountryLanguage

    @classmethod
    async def get_countries_code_by_languages(
        cls,
        db: AsyncSession,
        language_codes: List[str] = None,
    ) -> Dict[str, List[int]]:
        """Получает коды стран, связанных с указанными языками."""
        if not language_codes:
            language_codes = ['ru']

        query = (
            select(CountryLanguage)
            .join(CountryLanguage.language)
            .join(CountryLanguage.country)
            .where(Language.code.in_(language_codes))
            .options(
                joinedload(CountryLanguage.language),
                joinedload(CountryLanguage.country)
            )
        )
        try:
            result = await db.execute(query)
            country_links = result.scalars().all()

            result_dict = {}
            for link in country_links:
                lang_code = link.language.code
                if lang_code not in result_dict:
                    result_dict[lang_code] = []
                result_dict[lang_code].append(link.country.country_id)

            return result_dict
        except (SQLAlchemyError, Exception) as e:
            logging.error(f"Ошибка при получении страны: {e}")
