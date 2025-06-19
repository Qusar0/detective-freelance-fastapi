from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.api.dao.base import BaseDAO
from server.api.models.models import UserBalances
from server.api.scripts.sse_manager import publish_event


class UserBalancesDAO(BaseDAO):
    model = UserBalances

    @classmethod
    async def subtract_balance(cls, user_id: int, amount: float, channel: str, db: AsyncSession):
        result = await db.execute(
            select(UserBalances)
            .filter_by(user_id=user_id),
        )
        user_balance = result.scalars().first()

        if not user_balance:
            return

        user_balance.balance = round(
            user_balance.balance + (-amount),
            2,
        )

        await db.commit()

        event_data = {
            "event_type": "balance",
            "balance": user_balance.balance,
        }

        await publish_event(channel, event_data)
