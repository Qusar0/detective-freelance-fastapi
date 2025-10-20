from loguru import logger
from typing import List, Dict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from server.api.dao.base import BaseDAO
from server.api.models.models import QuerySearchCategory, QuerySearchCategoryType


class QuerySearchCategoryDAO(BaseDAO):
    model = QuerySearchCategory

    @classmethod
    async def add_search_categories(
        cls,
        db: AsyncSession,
        query_id: int,
        categories_str: str,
    ) -> bool:
        """Добавляет категории поиска для запроса."""
        if not categories_str:
            logger.error("Пустая строка категорий")
            return False

        try:
            categories = [cat.strip() for cat in categories_str.split(',') if cat.strip()]

            has_report = any('report' in cat.lower() for cat in categories)

            if has_report:
                categories = [cat for cat in categories if 'report' in cat.lower()]

            query = select(QuerySearchCategoryType).where(
                QuerySearchCategoryType.query_search_category_type.in_(categories),
            )
            result = await db.execute(query)
            category_types = result.scalars().all()

            if not category_types:
                logger.error("Не найдено ни одного типа категории")
                return False

            for category_type in category_types:
                new_category = QuerySearchCategory(
                    query_id=query_id,
                    search_category_type_id=category_type.id,
                )
                db.add(new_category)

            await db.commit()
            return True

        except SQLAlchemyError as e:
            await db.rollback()
            logger.error(f"Ошибка при добавлении категорий поиска: {e}")
            return False
        except Exception as e:
            logger.error(f"Неожиданная ошибка: {e}")
            return False

    @classmethod
    async def get_query_categories(
        cls,
        query_id: int,
        db: AsyncSession
    ) -> List[Dict[str, str]]:
        """Получает категории поиска для запроса."""
        try:
            result = await db.execute(
                select(
                    QuerySearchCategoryType.query_search_category_type_ru,
                    QuerySearchCategoryType.query_search_category_type,
                )
                .join(QuerySearchCategory.search_category_type)
                .where(QuerySearchCategory.query_id == query_id)
            )
            return [{"code": en_name.replace('company_', ''), "name": ru_name} for ru_name, en_name in result.all()]
        except SQLAlchemyError as e:
            logger.error(f"Ошибка получения категорий поиска: {e}")
            raise
