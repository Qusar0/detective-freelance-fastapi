import logging
from datetime import datetime

from sqlalchemy import select, delete

from server.api.database.database import get_db
from server.api.models.models import BalanceHistory, UserQueries, QueriesBalance, TextData, UserBalances
from server.api.scripts import utils
from server.api.scripts.sse_manager import publish_event
from server.api.services.file_storage import FileStorageService


async def get_user_query(query_id, db):
    result = await db.execute(
        select(UserQueries)
        .filter_by(query_id=query_id),
    )
    return result.scalars().first()


async def save_user_query(user_id, query_title, category):
    async with get_db() as session:
        now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

        user_query = UserQueries(
            user_id=user_id,
            query_unix_date="1980/01/01 00:00:00",
            query_created_at=now,
            query_title=query_title,
            query_status="pending",
            query_category=category
        )
        session.add(user_query)
        await session.commit()
        await session.refresh(user_query)

        return user_query


async def save_payment_to_history(user_id, price, query_id, db):
    balance_history = BalanceHistory(
        transaction_type='payment',
        amount=price,
        query_id=query_id,
        timestamp=datetime.now()
    )
    db.add(balance_history)
    await db.commit()


async def save_query_balance(query_id, price, db):
    balance = QueriesBalance(
        query_id=query_id,
        balance=price,
        transaction_date=datetime.now()
    )
    db.add(balance)
    await db.commit()


async def return_balance(user_id, query_id, amount, channel, db):
    result = await db.execute(
        select(BalanceHistory)
        .filter_by(
            query_id=query_id,
            transaction_type='payment',
        )
    )
    balance_history = result.scalars().first()
    if balance_history and balance_history.transaction_type != "returned":
        balance_history.transaction_type = 'returned'

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


async def save_html(html, query_id, db, file_storage: FileStorageService):
    try:
        file_path = await file_storage.save_query_data(query_id, html)
        
        text_data = TextData(query_id=query_id, file_path=file_path)
        db.add(text_data)
        await db.commit()
        
        return file_path
    except Exception as e:
        logging.error(f"Failed to save HTML for query {query_id}: {str(e)}")
        await db.rollback()
        raise


async def change_query_status(user_query, query_type, db):
    user_query.query_status = query_type
    await db.commit()


async def send_sse_notification(user_query, channel, db):
    event_data = {
        "message": {
            "status": user_query.query_status,
            "task_id": user_query.query_id,
            "task_category": user_query.query_category,
            "task_title": user_query.query_title,
            "task_created_at": str(user_query.query_created_at)
        }
    }

    event_id, event_type, created_time, event_status = await utils.save_event(
        event_data,
        user_query.query_id,
        db,
    )

    event_data.update({
        "event_id": event_id,
        "event_type": event_type,
        "created_time": str(created_time),
        "event_status": event_status
    })

    await publish_event(channel, event_data)


async def delete_query_by_id(query_id, db):
    try:
        user_query = await get_user_query(query_id, db)
        if user_query:
            await db.execute(delete(UserQueries).where(UserQueries.query_id == query_id))
            await db.commit()
            logging.info(f"Celery: Query {query_id} удалён автоматически.")
    except Exception as e:
        await db.rollback()
        logging.error(f"Ошибка при удалении query {query_id}: {str(e)}")
        raise
