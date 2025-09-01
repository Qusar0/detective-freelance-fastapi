from loguru import logger
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

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
        try:
            db.add(balance)
            await db.commit()
        except (SQLAlchemyError, Exception) as e:
            logger.error(f"Ошибка при сохранении баланса: {e}")
