from typing import Dict
import logging
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from server.api.dao.base import BaseDAO
from server.api.dao.user_queries import UserQueriesDAO
from server.api.models.models import KeywordType, QueriesData, Keywords, QueryDataKeywords


class QueryKeywordStatsDAO(BaseDAO):
    @classmethod
    async def get_keyword_stats(
        cls,
        query_id: int,
        db: AsyncSession
    ) -> Dict[str, int]:
        """Получает статистику по типам ключевых слов с учетом категории запроса"""
        try:
            query = await UserQueriesDAO.get_user_query(query_id, db)
            if not query:
                return {}

            query_category = query.query_category

            if query_category == 'company':
                type_filter = or_(
                    KeywordType.keyword_type_name.like('company_%'),
                    KeywordType.keyword_type_name == 'free word'
                )
            elif query_category == 'name':
                type_filter = or_(
                    ~KeywordType.keyword_type_name.like('company%'),
                    KeywordType.keyword_type_name == 'free word'
                )

            all_types_query = select(KeywordType.keyword_type_name).where(type_filter)
            all_types_result = await db.execute(all_types_query)
            all_types = {t[0]: 0 for t in all_types_result.all()}

            type_stats_query = (
                select(
                    KeywordType.keyword_type_name,
                    func.count(QueriesData.id)
                )
                .join(KeywordType.keywords)
                .join(Keywords.query_data_associations)
                .join(QueryDataKeywords.query_data)
                .where(
                    QueriesData.query_id == query_id,
                    type_filter,
                )
                .group_by(KeywordType.keyword_type_name)
            )

            type_stats_result = await db.execute(type_stats_query)

            for keyword_type, count in type_stats_result.all():
                all_types[keyword_type] = count

            subquery = (
                select(QueriesData.id)
                .join(QueriesData.keywords)
                .where(QueriesData.query_id == query_id)
                .group_by(QueriesData.id)
                .having(func.count(QueryDataKeywords.id) >= 3)
                .subquery()
            )

            main_count_result = await db.execute(
                select(func.count()).select_from(subquery)
            )
            main_count = main_count_result.scalar() or 0

            result_stats = all_types.copy()
            result_stats['main'] = main_count

            return result_stats

        except SQLAlchemyError as e:
            logging.error(f"Ошибка получения статистики ключевых слов: {e}")
            raise
