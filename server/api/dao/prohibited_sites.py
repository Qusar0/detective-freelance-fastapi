from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from server.api.dao.base import BaseDAO
from server.api.models.models import ProhibitedSites


class ProhibitedSitesDAO(BaseDAO):
    model = ProhibitedSites

    @classmethod
    async def add_sites_from_db(cls, user_prohibited_sites: list, db: AsyncSession) -> list:
        try:
            result = await db.execute(select(ProhibitedSites.site_link))
            sites_from_db = result.scalars().all()

            return list(set(sites_from_db + user_prohibited_sites))
        except (SQLAlchemyError, Exception) as e:
            logger.error(f"Ошибка при добавлении сайтов: {e}")
