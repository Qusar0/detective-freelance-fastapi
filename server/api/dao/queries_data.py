from typing import List, Optional
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
import logging

from server.api.models.models import QueriesData, KeywordType, Keywords, QueryDataKeywords
from server.api.dao.base import BaseDAO


class QueriesDataDAO(BaseDAO):
    model = QueriesData

    @classmethod
    async def get_query_data_count(
        cls,
        query_id: int,
        keyword_type_category: str,
        db: AsyncSession,
    ) -> int:
        """Получает общее количество записей для запроса с фильтрацией."""
        try:
            if keyword_type_category == 'main':
                count_query = (
                    select(func.count(QueriesData.id))
                    .where(QueriesData.query_id == query_id)
                    .where(
                        select(func.count(QueryDataKeywords.id))
                        .where(QueryDataKeywords.query_data_id == QueriesData.id)
                        .correlate(QueriesData)
                        .scalar_subquery() >= 3
                    )
                )
            else:
                base_query = cls._build_base_query(query_id, keyword_type_category)
                count_query = select(func.count()).select_from(base_query.alias())
            result = await db.execute(count_query)
            return result.scalar()
        except SQLAlchemyError as e:
            logging.error(f"Error counting query data: {e}")
            raise

    @classmethod
    async def get_paginated_query_data(
        cls,
        query_id: int,
        page: int,
        size: int,
        keyword_type_category: str,
        db: AsyncSession,
    ) -> List:
        """Получает пагинированные данные запроса с фильтрацией."""
        try:
            base_query = cls._build_base_query(query_id, keyword_type_category)
            paginated_query = (
                base_query
                .options(
                    joinedload(QueriesData.keywords).joinedload(QueryDataKeywords.original_keyword)
                )
                .order_by(QueriesData.created_at.desc())
                .limit(size)
                .offset((page - 1) * size)
                .distinct()
            )
            result = await db.execute(paginated_query)
            return result.unique().all()
        except SQLAlchemyError as e:
            logging.error(f"Error getting paginated query data: {e}")
            raise

    @classmethod
    def _build_base_query(cls, query_id: int, keyword_type_category: Optional[str] = None):
        """Строит базовый запрос с учетом фильтрации."""
        base_query = (
            select(QueriesData, KeywordType)
            .join(QueriesData.keywords)
            .join(QueryDataKeywords.original_keyword)
            .join(Keywords.keyword_type)
            .where(QueriesData.query_id == query_id)
        )

        if not keyword_type_category:
            return base_query

        SOCIAL_URLS = ['Вконтакте', 'Одноклассники', 'Facebook', 'Instagram', 'Telegram']
        DOCUMENT_TYPES = ['Word', 'PDF', 'Excel', 'Txt', 'PowerPoint']

        if keyword_type_category == 'socials':
            return base_query.where(QueriesData.resource_type.in_(SOCIAL_URLS))
        elif keyword_type_category == 'documents':
            return base_query.where(QueriesData.resource_type.in_(DOCUMENT_TYPES))
        elif keyword_type_category == 'main':
            keyword_count_subquery = (
                select(func.count(QueryDataKeywords.id))
                .where(QueryDataKeywords.query_data_id == QueriesData.id)
                .correlate(QueriesData)
                .scalar_subquery()
            )
            return base_query.where(keyword_count_subquery >= 3)
        else:
            return base_query.where(KeywordType.keyword_type_name == keyword_type_category)
