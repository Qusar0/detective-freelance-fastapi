from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.api.dao.base import BaseDAO
from server.api.models.irbis_models import PersonRoleType


class PersonRoleTypeDAO(BaseDAO):
    model = PersonRoleType

    @classmethod
    async def get_roles_map(
        cls,
        db: AsyncSession,
    ):
        """Получает все типы участников в виде словаря {код: регион}."""
        try:
            result = await db.execute(select(cls.model))
            person_roles = result.scalars().all()
            person_roles_map = {role.name: role for role in person_roles}
            return person_roles_map
        except Exception as e:
            logger.error(f"Ошибка при получении типов участников: {e}", exc_info=True)
            return {}

    @classmethod
    async def get_roles_with_short_map(
        cls,
        db: AsyncSession,
    ):
        """Получает все типы участников с коротким именем в виде словаря {код: регион}."""
        try:
            result = await db.execute(select(cls.model).where(cls.model.short_name != None))  # noqa: E711
            person_roles = result.scalars().all()
            person_roles_map = {role.short_name: role for role in person_roles}
            return person_roles_map
        except Exception as e:
            logger.error(f"Ошибка при получении типов участников с коротким именем: {e}", exc_info=True)
            return {}
