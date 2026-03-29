import math
from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from server.api.dao.base import BaseDAO
from server.api.models.models import UserBalanceHistory, UserQueries, BalanceTransactionType


class UserBalanceHistoryDAO(BaseDAO):
    model = UserBalanceHistory

    @classmethod
    def make_entry(
        cls,
        user_id: int,
        transaction_type: BalanceTransactionType,
        amount: float,
        query_id: int | None = None,
    ) -> UserBalanceHistory:
        return UserBalanceHistory(
            user_id=user_id,
            transaction_type=transaction_type,
            amount=amount,
            timestamp=datetime.now(),
            query_id=query_id,
        )

    @classmethod
    async def get_user_history(
        cls,
        user_id: int,
        page: int,
        size: int,
        db: AsyncSession,
    ) -> dict:
        base = (
            select(UserBalanceHistory, UserQueries.query_title)
            .outerjoin(UserQueries, UserBalanceHistory.query_id == UserQueries.query_id)
            .where(UserBalanceHistory.user_id == user_id)
        )

        total_result = await db.execute(
            select(func.count()).select_from(base.subquery())
        )
        total = total_result.scalar()

        rows = await db.execute(
            base
            .order_by(UserBalanceHistory.timestamp.desc())
            .limit(size)
            .offset(page * size)
        )

        items = []
        for record, query_title in rows.all():
            items.append({
                "id": record.id,
                "transaction_type": record.transaction_type,
                "amount": record.amount,
                "timestamp": record.timestamp,
                "query_id": record.query_id,
                "query_title": query_title,
            })

        return {
            "items": items,
            "total": total,
            "page": page,
            "size": size,
            "total_pages": math.ceil(total / size) if size else 0,
        }
