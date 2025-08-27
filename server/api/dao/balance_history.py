from loguru import logger
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from server.api.models.models import BalanceHistory, UserBalances
from server.api.scripts.sse_manager import publish_event
from server.api.dao.base import BaseDAO


class BalanceHistoryDAO(BaseDAO):
    model = BalanceHistory

    @classmethod
    async def save_payment_to_history(cls, price, query_id, db):
        balance_history = BalanceHistory(
            transaction_type='payment',
            amount=price,
            query_id=query_id,
            timestamp=datetime.now()
        )
        try:
            db.add(balance_history)
            await db.commit()
        except (SQLAlchemyError, Exception) as e:
            logger.error(f"Ошибка при сохранении истории: {e}")

    @classmethod
    async def return_balance(cls, user_id, query_id, amount, channel, db):
        try:
            result = await db.execute(
                select(BalanceHistory)
                .filter_by(
                    query_id=query_id,
                    transaction_type='payment',
                )
            )
            balance_history = result.scalars().first()
        except (SQLAlchemyError, Exception) as e:
            logger.error(f"Ошибка при получении истории: {e}")

        if balance_history and balance_history.transaction_type != "returned":
            balance_history.transaction_type = 'returned'
            try:
                result = await db.execute(
                    select(UserBalances)
                    .filter_by(user_id=user_id),
                )
                user_balance = result.scalars().first()
                user_balance.balance = round(user_balance.balance + amount, 2)

                db.add(balance_history)
                await db.commit()

                await publish_event(channel, {
                    "event_type": "balance",
                    "balance": user_balance.balance
                })
            except (SQLAlchemyError, Exception) as e:
                logger.error(f"Ошибка при обновлении баланса: {e}")
                await db.rollback()
