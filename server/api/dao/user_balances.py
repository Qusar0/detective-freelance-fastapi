from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from server.api.dao.base import BaseDAO
from server.api.models.models import UserBalances
from server.api.scripts.sse_manager import publish_event


class InsufficientFundsError(Exception):
    def __init__(self, current_balance: float, required_amount: float):
        self.current_balance = current_balance
        self.required_amount = required_amount
        super().__init__(f"Недостаточно средств. Баланс: {current_balance}, требуется: {required_amount}")


class UserBalancesDAO(BaseDAO):
    model = UserBalances

    @classmethod
    async def subtract_balance(cls, user_id: int, amount: float, channel: str, db: AsyncSession):
        try:
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

            if user_balance.balance < amount:
                raise InsufficientFundsError(
                    current_balance=user_balance.balance,
                    required_amount=amount
                )

            await db.commit()

            event_data = {
                "event_type": "balance",
                "balance": user_balance.balance,
            }

            await publish_event(channel, event_data)
        except InsufficientFundsError:
            raise InsufficientFundsError(
                    current_balance=user_balance.balance,
                    required_amount=amount
                )
        except (SQLAlchemyError, Exception) as e:
            logger.error(f"Ошибка при списании с баланса: {e}")
            await db.rollback()
