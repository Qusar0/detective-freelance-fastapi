import logging
from datetime import datetime
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from server.api.database.database import get_db
from server.api.dao.base import BaseDAO
from server.api.models.models import UserQueries


class UserQueriesDAO(BaseDAO):
    model = UserQueries

    @classmethod
    async def get_user_query(cls, query_id, db):
        result = await db.execute(
            select(UserQueries)
            .filter_by(query_id=query_id),
        )
        return result.scalars().first()

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
            session.add(user_query)
            await session.commit()
            await session.refresh(user_query)

            return user_query
        
    @classmethod
    async def change_query_status(cls, user_query, query_type, db):
        user_query.query_status = query_type
        await db.commit()


    @classmethod
    async def delete_query_by_id(cls, query_id, db):
        try:
            user_query = await cls.get_user_query(query_id, db)
            if user_query:
                await db.execute(delete(UserQueries).where(UserQueries.query_id == query_id))
                await db.commit()
                logging.info(f"Celery: Query {query_id} удалён автоматически.")
        except Exception as e:
            await db.rollback()
            logging.error(f"Ошибка при удалении query {query_id}: {str(e)}")
            raise

    @classmethod
    async def get_queries_page(cls, filter: tuple, page: int = 0, page_size: int = 20, db: AsyncSession = None):
        stmt = (
            select(UserQueries)
            .filter_by(user_id=filter[0], query_category=filter[1])
            .order_by(UserQueries.query_created_at.desc())
        )

        if page_size:
            stmt = stmt.limit(page_size)
        if page:
            stmt = stmt.offset(page * page_size)

        result = await db.execute(stmt)
        queries = result.scalars().all()

        return queries