import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from server.api.dao.base import BaseDAO
from server.api.models.models import Language


class LanguageDAO(BaseDAO):
    model = Language

    @classmethod
    async def get_languages_by_code(
        cls,
        db: AsyncSession,
        language_codes: List[str] = None,
    ) -> List[dict]:
        """Получает информацию о языках по их кодам."""
        if not language_codes:
            language_codes = ['ru']

        query = (
            select(Language)
            .where(Language.code.in_(language_codes))
        )

        result = await db.execute(query)
        languages = result.scalars().all()

        return [lang.russian_name for lang in languages]