from loguru import logger
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
            logger.debug(f"Запрос IrbisPerson для user_id: {user_id}, query_id: {query_id}")

            query = await UserQueriesDAO.get_query_by_id(
                user_id,
                query_id,
                db,
            )

            if not query:
                logger.warning(f"Запрос не найден для user_id: {user_id}, query_id: {query_id}")
                return None

            result = await db.execute(
                select(IrbisPerson)
                .filter_by(query_id=query_id),
            )

            irbis_person = result.scalars().first()

            if irbis_person:
                logger.debug(f"Найден IrbisPerson: {irbis_person.id} для query_id: {query_id}")
            else:
                logger.warning(f"IrbisPerson не найден для query_id: {query_id}")
            return irbis_person
        except (SQLAlchemyError, Exception) as e:
            logger.error(f"Ошибка при получении person uuid: {e}", exc_info=True)
            await db.rollback()
            return None

    @classmethod
    async def get_count_info(cls, person_uuid_id: int, db: AsyncSession):
        try:
            logger.debug(f"Запрос статистики для person_uuid_id: {person_uuid_id}")
            # TODO: Логика получения статистики
            pass

        except Exception as e:
            logger.error(f"Ошибка при получении статистики запроса: {e}", exc_info=True)
            await db.rollback()
