import logging
from datetime import datetime
from sqlalchemy import select, delete

from server.api.database.database import get_db
from server.api.models.models import BalanceHistory, UserQueries, QueriesBalance, TextData, UserBalances
from server.api.scripts import utils
from server.api.scripts.sse_manager import publish_event
from server.api.services.file_storage import FileStorageService
from server.api.dao.base import BaseDAO
from server.api.models.models import QueriesBalance

class QueriesBalanceDAO(BaseDAO):
    model = QueriesBalance


async def save_query_balance(query_id, price, db):
    balance = QueriesBalance(
        query_id=query_id,
        balance=price,
        transaction_date=datetime.now()
    )
    db.add(balance)
    await db.commit()