from loguru import logger
from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class BaseDAO:
    model = None

    @classmethod
    async def add(cls, db: AsyncSession, **data):
        try:
            query = insert(cls.model).values(**data).returning(cls.model)
            result = await db.execute(query)
            await db.commit()
            return result.scalars().first()
        except (SQLAlchemyError, Exception) as e:
            logger.error(f"Ошибка SQL запроса: {e}")

    @classmethod
    async def _delete(cls, db: AsyncSession, **filter_by):
        query = delete(cls.model).filter_by(**filter_by).returning(cls.model)
        try:
            await db.execute(query)
            await db.commit()
        except (SQLAlchemyError, Exception) as e:
            logger.error(f"Ошибка SQL запроса: {e}")

    @classmethod
    async def delete_all(cls, db: AsyncSession, **filter_by):
        query = delete(cls.model).filter_by(**filter_by)
        try:
            await db.execute(query)
            await db.commit()
            return True
        except (SQLAlchemyError, Exception) as e:
            logger.error(f"Ошибка SQL запроса: {e}")
            return False

    @classmethod
    async def find_one_or_none(cls, db: AsyncSession, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await db.execute(query)
        return result.scalars().one_or_none()

    @classmethod
    async def find_all(cls, db: AsyncSession, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await db.execute(query)
        return result.scalars().all()

    @classmethod
    async def _update(cls, db: AsyncSession, filter_by: dict, **update_data):
        try:
            if not isinstance(filter_by, dict):
                raise TypeError("filter_by должен быть словарем")
            stmt = (
                update(cls.model)
                .filter_by(**filter_by)
                .values(**update_data)
                .execution_options(synchronize_session='fetch')
                .returning(cls.model)
            )
            result = await db.execute(stmt)
            await db.commit()
            return result.scalars().first()
        except (SQLAlchemyError, Exception) as e:
            logger.error(f"Ошибка SQL запроса: {e}")
