from typing import List
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from server.api.dao.base import BaseDAO
from server.api.models.models import ProhibitedSites, ProhibitedPhoneSites


class ProhibitedSitesDAO(BaseDAO):
    model = ProhibitedSites

    @classmethod
    async def add_sites_from_db(cls, user_prohibited_sites: List, db: AsyncSession) -> List:
        try:
            logger.debug(f"Добавление сайтов из БД к пользовательским: {len(user_prohibited_sites)} сайтов")

            result = await db.execute(select(ProhibitedSites.site_link))
            sites_from_db = result.scalars().all()
            logger.debug(f"Получено {len(sites_from_db)} сайтов из БД")

            combined_sites = list(set(sites_from_db + user_prohibited_sites))
            return combined_sites
        except (SQLAlchemyError, Exception) as e:
            logger.error(f"Ошибка при добавлении сайтов: {e}")
            return user_prohibited_sites

    @classmethod
    async def select_needless_sites(cls, db: AsyncSession):
        try:
            logger.debug("Запрос запрещенных сайтов для телефонов")

            result = await db.execute(select(ProhibitedPhoneSites.site_link))
            sites = result.scalars().all()

            logger.info(f"Получено {len(sites)} запрещенных сайтов для телефонов")
            return sites

        except (SQLAlchemyError, Exception) as e:
            logger.error(f"Ошибка при получении запрещенных сайтов для телефонов: {e}")
            return []
