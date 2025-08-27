from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional

from server.api.dao.base import BaseDAO
from server.api.models.models import Language, QueryTranslationLanguages


class LanguageDAO(BaseDAO):
    model = Language

    @classmethod
    async def get_languages_by_code(
        cls,
        db: AsyncSession,
        language_codes: Optional[List[str]] = None,
    ) -> Optional[List[dict]]:
        """Получает информацию о языках по их кодам."""
        if not language_codes:
            language_codes = ['ru']

        query = (
            select(Language)
            .where(Language.code.in_(language_codes))
        )
        try:
            result = await db.execute(query)
            languages = result.scalars().all()

            return [lang.russian_name for lang in languages]
        except (SQLAlchemyError, Exception) as e:
            logger.error(f"Ошибка при получении кода: {e}")

    @classmethod
    async def save_query_languages(
        cls,
        db: AsyncSession,
        query_id: int,
        language_codes: Optional[List[str]] = None,
    ) -> bool:
        """Сохраняет языки для перевода запроса."""
        if not language_codes:
            language_codes = ['ru']

        try:
            query = select(Language).where(Language.code.in_(language_codes))
            result = await db.execute(query)
            languages = result.scalars().all()

            if not languages:
                logger.error("Не найдено языков с указанными кодами")
                return False

            for language in languages:
                translation_lang = QueryTranslationLanguages(
                    query_id=query_id,
                    language_id=language.id
                )
                db.add(translation_lang)

            await db.commit()
            return True

        except SQLAlchemyError as e:
            await db.rollback()
            logger.error(f"Ошибка при сохранении языков перевода: {e}")
            return False
        except Exception as e:
            logger.error(f"Неожиданная ошибка: {e}")
            return False
