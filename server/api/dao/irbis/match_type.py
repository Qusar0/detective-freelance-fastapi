from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.api.dao.base import BaseDAO
from server.api.models.irbis_models import MatchType


class MatchTypeDAO(BaseDAO):
    model = MatchType

    @classmethod
    async def get_type_by_name(
        cls,
        name: str,
        db: AsyncSession,
    ):
        """Получает пагинированные данные запроса."""
        try:
            result = await db.execute(
                select(MatchType)
                .where(MatchType.name == name)
            )
            return result.scalar_one_or_none()
        except:
            pass
