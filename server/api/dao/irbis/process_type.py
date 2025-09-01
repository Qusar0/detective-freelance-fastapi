from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.api.dao.base import BaseDAO
from server.api.models.irbis_models import ProcessType


class ProcessTypeDAO(BaseDAO):
    model = ProcessType

    @classmethod
    async def get_process_type_by_code(
        cls,
        process_type_code: str,
        db: AsyncSession,
    ):
        """Получает тип поиска по коду."""
        try:
            result = await db.execute(
                select(ProcessType)
                .where(ProcessType.code == process_type_code)
            )
            process_type = result.scalar_one_or_none()

            return process_type
        except Exception as e:
            logger.error(f"Ошибка при получении типа процесса по коду {process_type_code}: {e}", exc_info=True)
            return None
