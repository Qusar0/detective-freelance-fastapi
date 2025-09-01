from loguru import logger
from datetime import datetime
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from server.api.models.models import (
    QueriesData,
    AdditionalQueryWord,
    QuerySearchCategory,
    QueryTranslationLanguages,
    Events,
    TextData,
)
from server.api.database.database import get_db
from server.api.dao.base import BaseDAO
from server.api.models.models import UserQueries
from server.api.services.file_storage import FileStorageService


class UserQueriesDAO(BaseDAO):
    model = UserQueries

    @classmethod
    async def get_user_query(cls, query_id, db):
        try:
            result = await db.execute(
                select(UserQueries)
                .filter_by(query_id=query_id),
            )
            return result.scalars().first()
        except (SQLAlchemyError, Exception) as e:
            logger.error(f"Ошибка при получении запроса пользователя: {e}")

    @classmethod
    async def save_user_query(cls, user_id, query_title, category):
        async with get_db() as session:
            now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

            user_query = UserQueries(
                user_id=user_id,
                query_unix_date="1980/01/01 00:00:00",
                query_created_at=now,
                query_title=query_title,
                query_status="pending",
                query_category=category
            )
            try:
                session.add(user_query)
                await session.commit()
                await session.refresh(user_query)

                return user_query
            except (SQLAlchemyError, Exception) as e:
                logger.error(f"Ошибка при сохранении запроса пользователя: {e}")

    @classmethod
    async def change_query_status(cls, user_query, query_type, db):
        user_query.query_status = query_type
        try:
            await db.commit()
        except (SQLAlchemyError, Exception) as e:
            logger.error(f"Ошибка при смене статуса запроса: {e}")

    @classmethod
    async def delete_query_info_by_id(cls, query_id, db):
        try:
            user_query = await cls.get_user_query(query_id, db)
            if user_query:
                file_storage = FileStorageService()
                result = await db.execute(select(TextData).where(TextData.query_id == query_id))
                text_data = result.scalars().first()
                if text_data and text_data.file_path:
                    try:
                        await file_storage.delete_query_data(text_data.file_path)
                        logger.info(f"Файл {text_data.file_path} успешно удалён.")
                    except Exception as e:
                        logger.error(f"Ошибка при удалении файла {text_data.file_path}: {e}")
                for table in [QueriesData, AdditionalQueryWord, QuerySearchCategory, QueryTranslationLanguages, Events, TextData]:
                    await db.execute(delete(table).where(table.query_id == query_id))
                user_query.deleted_at = datetime.now()
                logger.info(f"Данные для query {query_id} удалены. Установлен deleted_at: {user_query.deleted_at}.")
        except SQLAlchemyError as e:
            logger.error(f"Ошибка базы данных при удалении query {query_id}: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Неожиданная ошибка при удалении query {query_id}: {str(e)}")
            raise e

    @classmethod
    async def get_queries_page(
        cls,
        user_id: int,
        query_category: str,
        page: int,
        db: AsyncSession,
        page_size: int = 10,
    ):
        stmt = (
            select(UserQueries)
            .options(
                selectinload(UserQueries.queries_balances)
            )
            .where(UserQueries.deleted_at == None)  # noqa: E711
            .filter_by(user_id=user_id, query_category=query_category)
            .order_by(UserQueries.query_created_at.desc())
        )

        if page_size:
            stmt = stmt.limit(page_size)
        if page:
            stmt = stmt.offset(page * page_size)
        try:
            result = await db.execute(stmt)
            queries = result.scalars().all()

            return queries
        except (SQLAlchemyError, Exception) as e:
            logger.error(f"Ошибка при получении страницы запроса: {e}")

    @classmethod
    async def get_query_by_id(cls, user_id: int, query_id, db: AsyncSession):
        query = await db.execute(
            select(UserQueries)
            .where(
                UserQueries.query_id == query_id,
                UserQueries.user_id == user_id
            )
        )
        return query.scalar()
