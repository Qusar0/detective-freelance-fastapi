from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy import select, func, tuple_
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger

from server.api.models.models import QueriesData, KeywordType, Keywords, QueryDataKeywords
from server.api.dao.base import BaseDAO
from server.api.dao.keywords import KeywordsDAO
from server.api.dao.user_queries import UserQueriesDAO


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
                query = await UserQueriesDAO.get_user_query(query_id, db)
                query_category = query.query_category

                if keyword_type_category in {'reputation', 'negativ', 'relations'} and query_category == 'company':
                    keyword_type_category = f'company_{keyword_type_category}'

                base_query = cls._build_base_query(query_id, keyword_type_category)
                count_query = select(func.count()).select_from(base_query.alias())
            result = await db.execute(count_query)
            return result.scalar()
        except SQLAlchemyError as e:
            logger.error(f"Error counting query data: {e}")
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
            query = await UserQueriesDAO.get_user_query(query_id, db)
            query_category = query.query_category

            if keyword_type_category in {'reputation', 'negativ', 'relations'} and query_category == 'company':
                keyword_type_category = f'company_{keyword_type_category}'

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
            logger.error(f"Error getting paginated query data: {e}")
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

    @classmethod
    async def get_fullname_count(
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
                    .where(
                        QueriesData.query_id == query_id,
                        QueriesData.is_fullname == True,  # noqa: E712
                    )
                    .where(
                        select(func.count(QueryDataKeywords.id))
                        .where(QueryDataKeywords.query_data_id == QueriesData.id)
                        .correlate(QueriesData)
                        .scalar_subquery() >= 3
                    )
                )
            else:
                base_query = cls._build_base_query(query_id, keyword_type_category)
                base_query = base_query.where(QueriesData.is_fullname == True)  # noqa: E712
                count_query = select(func.count()).select_from(base_query.alias())
            result = await db.execute(count_query)
            return result.scalar()
        except SQLAlchemyError as e:
            logger.error(f"Error counting query data: {e}")
            raise

    @classmethod
    async def bulk_save_query_results(
        cls,
        query_id: int,
        raw_data: Dict[str, Dict[str, Any]],
        db: AsyncSession,
        batch_size: int = 200,
    ) -> None:
        """Сохраняет результаты поиска в таблицу queries_data с оптимизацией через bulk операции."""
        try:
            keyword_lookup: Dict[Tuple[str, str], Optional[int]] = {}
            for item in raw_data.values():
                keywords = item.get('keywords', set())
                for keyword, original_keyword, keyword_type in keywords:
                    if (original_keyword, keyword_type) not in keyword_lookup:
                        keyword_lookup[(original_keyword, keyword_type)] = None

            if keyword_lookup:
                keyword_pairs = list(keyword_lookup.keys())
                batch_size_lookup = 500
                for i in range(0, len(keyword_pairs), batch_size_lookup):
                    batch_pairs = keyword_pairs[i:i + batch_size_lookup]

                    result = await db.execute(
                        select(Keywords.id, Keywords.word, KeywordType.keyword_type_name)
                        .join(KeywordType)
                        .where(
                            tuple_(Keywords.word, KeywordType.keyword_type_name).in_(batch_pairs)
                        )
                    )

                    for kw_id, kw_word, kw_type in result.all():
                        keyword_lookup[(kw_word, kw_type)] = kw_id

            items = list(raw_data.items())

            for batch_start in range(0, len(items), batch_size):
                batch = items[batch_start:batch_start + batch_size]
                query_data_list = []
                keyword_data_list = []

                for url, item in batch:
                    title = item.get('title')
                    snippet = item.get('snippet')
                    keywords = item.get('keywords', set())
                    publication_date = item.get('pubDate') or item.get('publication_date')
                    resource_type = item.get('resource_type')
                    is_fullname = item.get('is_fullname')

                    query_data = QueriesData(
                        query_id=query_id,
                        title=title,
                        info=snippet,
                        link=url,
                        publication_date=publication_date,
                        resource_type=resource_type,
                        is_fullname=is_fullname,
                    )
                    query_data_list.append(query_data)

                    for keyword, original_keyword, keyword_type in keywords:
                        keyword_data_list.append((query_data, keyword, original_keyword, keyword_type))

                db.add_all(query_data_list)
                await db.flush()

                query_keyword_objects = []
                for query_data, keyword, original_keyword, keyword_type in keyword_data_list:
                    original_keyword_id = keyword_lookup.get((original_keyword, keyword_type))
                    if original_keyword_id:
                        query_data_keyword = QueryDataKeywords(
                            query_data_id=query_data.id,
                            keyword=keyword,
                            original_keyword_id=original_keyword_id,
                        )
                        query_keyword_objects.append(query_data_keyword)

                if query_keyword_objects:
                    db.add_all(query_keyword_objects)
                    await db.flush()

            await db.commit()
            logger.info(f"Сохраненные необработанные данные для запроса {query_id} - {len(raw_data)} записей")

        except Exception as e:
            logger.error(f"Не удалось сохранить необработанные данные: {e}")
            await db.rollback()
            raise

    @classmethod
    async def bulk_save_simple_results(
        cls,
        query_id: int,
        raw_data: Dict[str, Dict[str, Any]],
        keyword_word: str,
        keyword_type: str,
        db: AsyncSession,
        batch_size: int = 200,
    ) -> None:
        """Сохраняет результаты поиска с одним ключевым словом (для number и email)."""
        try:
            original_keyword_id = await KeywordsDAO.get_keyword_id(db, keyword_word, keyword_type)

            if not original_keyword_id:
                logger.warning(f"Keyword '{keyword_word}' с типом '{keyword_type}' не найден")

            items = list(raw_data.items())

            for batch_start in range(0, len(items), batch_size):
                batch = items[batch_start:batch_start + batch_size]
                query_data_list = []
                query_keyword_objects = []

                for url, item in batch:
                    title = item.get('raw_title') or item.get('title')
                    snippet = item.get('raw_snippet') or item.get('snippet')
                    publication_date = item.get('pubDate')

                    query_data = QueriesData(
                        query_id=query_id,
                        title=title,
                        info=snippet,
                        link=url,
                        publication_date=publication_date,
                    )
                    query_data_list.append(query_data)

                db.add_all(query_data_list)
                await db.flush()

                if original_keyword_id:
                    for query_data in query_data_list:
                        query_data_keyword = QueryDataKeywords(
                            query_data_id=query_data.id,
                            keyword='ключевых слов нет',
                            original_keyword_id=original_keyword_id,
                        )
                        query_keyword_objects.append(query_data_keyword)

                    if query_keyword_objects:
                        db.add_all(query_keyword_objects)
                        await db.flush()

            await db.commit()
        except Exception as e:
            logger.error(f"Не удалось сохранить необработанные данные: {e}")
            await db.rollback()
            raise
