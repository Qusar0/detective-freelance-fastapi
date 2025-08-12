from typing import List, Dict
import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from server.api.dao.base import BaseDAO
from server.api.models.models import Language, QueryTranslationLanguages


class QueryTranslationLanguagesDAO(BaseDAO):
    @classmethod
    async def get_query_languages(
        cls,
        query_id: int,
        db: AsyncSession
    ) -> List[Dict[str, str]]:
        """Получает языки, связанные с запросом."""
        try:
            result = await db.execute(
                select(Language.code, Language.russian_name)
                .join(QueryTranslationLanguages.language)
                .where(QueryTranslationLanguages.query_id == query_id)
            )
            return [{"code": code, "name": name} for code, name in result.all()]
        except SQLAlchemyError as e:
            logging.error(f"Ошибка получения языков поиска: {e}")
            raise
