from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.api.models.irbis_models import (
    ArbitrationCourtCaseTypes,
)
from server.api.dao.base import BaseDAO
from loguru import logger


class ArbitrationCourtCaseTypesDAO(BaseDAO):
    model = ArbitrationCourtCaseTypes

    @classmethod
    async def get_case_types_map(
        cls,
        db: AsyncSession,
    ):
        """Получает типы дел в формате словаря."""
        try:
            result = await db.execute(select(cls.model))
            case_types = result.scalars().all()
            case_type_map = {case_type.code: case_type for case_type in case_types}
            return case_type_map
        except Exception as e:
            logger.error(f"Ошибка при получении типов дел: {e}", exc_info=True)
            return {}
