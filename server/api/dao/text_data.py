from loguru import logger
from sqlalchemy.exc import SQLAlchemyError

from server.api.services.file_storage import FileStorageService
from server.api.dao.base import BaseDAO
from server.api.models.models import TextData


class TextDataDAO(BaseDAO):
    model = TextData

    @classmethod
    async def save_html(cls, html, query_id, db, file_storage: FileStorageService):
        try:
            file_path = await file_storage.save_query_data(query_id, html)

            text_data = TextData(query_id=query_id, file_path=file_path)
            db.add(text_data)
            await db.commit()

            return file_path
        except (SQLAlchemyError, Exception) as e:
            logger.error(f"Failed to save HTML for query {query_id}: {str(e)}")
            await db.rollback()
            raise
