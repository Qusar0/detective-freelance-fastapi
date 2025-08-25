from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.api.models.irbis_models import (
    CourtGeneralFacesTable,
)
from server.api.dao.base import BaseDAO


class CourtGeneralFacesDAO(BaseDAO):
    model = CourtGeneralFacesTable

    @classmethod
    async def get_faces_by_case_id(
        cls,
        case_id: int,
        db: AsyncSession,
    ):
        """Получает пагинированные данные запроса."""
        try:
            result = await db.execute(
                select(CourtGeneralFacesTable)
                .filter_by(case_id=case_id)
            )

            faces = result.all()

            if not faces:
                return None

            return faces
        except:
            pass
