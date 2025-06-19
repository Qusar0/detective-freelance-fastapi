import logging
from datetime import datetime
from sqlalchemy import select, delete

from server.api.database.database import get_db
from server.api.models.models import BalanceHistory, UserQueries, QueriesBalance, TextData, UserBalances
from server.api.scripts import utils
from server.api.scripts.sse_manager import publish_event
from server.api.services.file_storage import FileStorageService
from server.api.dao.base import BaseDAO
from server.api.models.models import TextData

class TextDataDAO(BaseDAO):
    model = TextData


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