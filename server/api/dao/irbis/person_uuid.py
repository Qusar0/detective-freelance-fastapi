import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from server.api.dao.base import BaseDAO
from server.api.dao.user_queries import UserQueriesDAO
from server.api.models.irbis_models import IrbisPerson


class IrbisPersonDAO(BaseDAO):
    model = IrbisPerson

    @classmethod
    async def get_irbis_person(cls, user_id: int, query_id: int, db: AsyncSession):
        try:
            query = await UserQueriesDAO.get_query_by_id(
                user_id,
                query_id,
                db,
            )

            if not query:
                return None

            result = await db.execute(
                select(IrbisPerson)
                .filter_by(query_id=query_id),
            )

            return result.scalars().first()
        except (SQLAlchemyError, Exception) as e:
            logging.error(f"Ошибка при получении person uuid: {e}")
            await db.rollback()

    @classmethod
    async def get_count_info(cls, person_uuid_id: int, db: AsyncSession):
        try:
            pass
        except Exception as e:
            logging.error(f"Ошибка при получении статистики запроса: {e}")
            await db.rollback()
