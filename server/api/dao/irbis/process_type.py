from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.api.dao.base import BaseDAO
from server.api.models.irbis_models import ProcessType


class ProcessTypeDAO(BaseDAO):
    model = ProcessType

    @classmethod
    async def get_process_types_map(
        cls,
        db: AsyncSession,
    ):
        """Получает типы поиска."""
        try:
            result = await db.execute(select(cls.model))
            process_types = result.scalars().all()
            process_type_map = {process_type.code: process_type for process_type in process_types}
            return process_type_map
        except Exception as e:
            logger.error(f"Ошибка при получении типов процесса: {e}", exc_info=True)
            return {}
