from typing import List, Dict
import logging
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from server.api.dao.base import BaseDAO
from server.api.models.models import KeywordType, QueriesData


class QueryKeywordStatsDAO(BaseDAO):
    @classmethod
    async def get_keyword_stats(
        cls,
        query_id: int,
        db: AsyncSession
    ) -> Dict[str, int]:
        """Получает статистику по типам ключевых слов"""
        try:
            result = await db.execute(
                select(
                    KeywordType.keyword_type_name,
                    func.count(QueriesData.id)
                )
                .join(QueriesData.keyword_type)
                .where(QueriesData.query_id == query_id)
                .group_by(KeywordType.keyword_type_name)
            )
            return {k: v for k, v in result.all()}
        except SQLAlchemyError as e:
            logging.error(f"Ошибка получения статистики ключевых слов: {e}")
            raise

    @classmethod
    async def get_free_words(
        cls,
        query_id: int,
        db: AsyncSession
    ) -> List[str]:
        """Получает список свободных слов для запроса"""
        try:
            result = await db.execute(
                select(QueriesData.keyword)
                .distinct()
                .join(QueriesData.keyword_type)
                .where(
                    QueriesData.query_id == query_id,
                    KeywordType.keyword_type_name == "free word",
                    QueriesData.keyword.isnot(None)
                )
            )
            return [word[0] for word in result.all() if word[0]]
        except SQLAlchemyError as e:
            logging.error(f"Error getting free words: {e}")
            raise
