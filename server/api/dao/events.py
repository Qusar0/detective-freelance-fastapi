import logging
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from server.api.dao.base import BaseDAO
from server.api.models.models import Events


class EventsDAO(BaseDAO):
    model = Events

    @classmethod
    async def save_event(cls, data: str, query_id: int, db: AsyncSession):
        now = datetime.now()

        user_query = Events(
            event_type="test",
            query_id=query_id,
            created_time=now,
            additional_data=data,
            event_status="unseen"
        )

        db.add(user_query)
        await db.commit()
        await db.refresh(user_query)

        return user_query.event_id, user_query.event_type, user_query.created_time, user_query.event_status