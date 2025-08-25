from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from server.api.models.irbis_models import (
    CourtGeneralJurFullTable,
)
from server.api.dao.base import BaseDAO


class CourtGeneralJurDAO(BaseDAO):
    model = CourtGeneralJurFullTable

    @classmethod
    async def get_paginated_query_data(
        cls,
        irbis_person_id: int,
        page: int,
        size: int,
        db: AsyncSession,
    ):
        """Получает пагинированные данные запроса."""
        try:
            result = await db.execute(
                select(CourtGeneralJurFullTable)
                .options(
                    selectinload(CourtGeneralJurFullTable.faces),
                    selectinload(CourtGeneralJurFullTable.progress),
                )
                .filter_by(irbis_person_id=irbis_person_id)
                .limit(size)
                .offset((page - 1) * size)
            )

            return result.unique().scalars().all()
        except:
            pass
