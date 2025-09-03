from loguru import logger
from sqlalchemy import update, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from server.api.dao.base import BaseDAO
from server.api.models.models import Users


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def update_last_visit(cls, user_id: int, db: AsyncSession):
        try:
            await db.execute(
                update(Users)
                .where(Users.id == user_id)
                .values(last_visited=func.now())
            )
            await db.commit()
        except (SQLAlchemyError, Exception) as e:
            logger.error(f"Ошибка обновления последнего посещения: {e}")
            await db.rollback()
