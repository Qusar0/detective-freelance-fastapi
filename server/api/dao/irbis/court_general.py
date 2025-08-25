from typing import List, Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
import logging

from server.api.models.irbis_models import (
    CourtGeneralFacesTable,
    CourtGeneralHeaderTable,
    CourtGeneralJurFullTable,
    CourtGeneralProgressTable,
)
from server.api.dao.base import BaseDAO


class CourtGeneralDAO(BaseDAO):
    model = CourtGeneralJurFullTable

    @classmethod
    async def get_paginated_query_data(
        cls,
        person_uuid_id: int,
        page: int,
        size: int,
        db: AsyncSession,
    ):
        """Получает пагинированные данные запроса."""
        try:
            
        except:
            pass
    
    @classmethod
    async def get_