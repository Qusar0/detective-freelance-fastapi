import logging
from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import SQLAlchemyError

from server.api.database.database import get_db


class BaseDAO:
    model = None

    @classmethod
    async def add(cls, **data):
        try:
            query = insert(cls.model).values(**data).returning(cls.model)
            async with get_db() as session:
                result = await session.execute(query)
                await session.commit()
                return result.scalars().first()
        except (SQLAlchemyError, Exception) as e:
            logging.error(f"SQL error: {e}")

    @classmethod
    async def _delete(cls, **filter_by):
        query = delete(cls.model).filter_by(**filter_by).returning(cls.model)
        try:
            async with get_db() as session:
                await session.execute(query)
                await session.commit()
        except (SQLAlchemyError, Exception) as e:
            logging.error(f"SQL error: {e}")

    @classmethod
    async def delete_all(cls, **filter_by):
        query = delete(cls.model).filter_by(**filter_by)
        try:
            async with get_db() as session:
                await session.execute(query)
                await session.commit()
                return True
        except (SQLAlchemyError, Exception) as e:
            logging.error(f"SQL error: {e}")
            return False

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        async with get_db() as session:
            result = await session.execute(query)
            return result.scalars().one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        async with get_db() as session:
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def _update(cls, filter_by: dict, **update_data):
        if not isinstance(filter_by, dict):
            raise TypeError("filter_by должен быть словарем")
        stmt = (
            update(cls.model)
            .filter_by(**filter_by)
            .values(**update_data)
            .execution_options(synchronize_session='fetch')
            .returning(cls.model)
        )
        try:
            async with get_db() as session:
                result = await session.execute(stmt)
                await session.commit()
                return result.scalars().first()
        except (SQLAlchemyError, Exception) as e:
            logging.error(f"SQL error: {e}")
