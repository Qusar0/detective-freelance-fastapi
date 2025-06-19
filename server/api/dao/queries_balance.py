from datetime import datetime

from server.api.dao.base import BaseDAO
from server.api.models.models import QueriesBalance


class QueriesBalanceDAO(BaseDAO):
    model = QueriesBalance

    @classmethod
    async def save_query_balance(cls, query_id, price, db):
        balance = QueriesBalance(
            query_id=query_id,
            balance=price,
            transaction_date=datetime.now()
        )
        db.add(balance)
        await db.commit()
