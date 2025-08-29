# Скрипт для периодической очистки данных старых запросов
import asyncio
from datetime import datetime, timedelta
import logging

from server.api.database.database import async_session
from server.api.dao.user_queries import UserQueriesDAO
from server.api.models.models import UserQueries

logging.basicConfig(level=logging.INFO)

async def cleanup_old_queries():
    while True:
        try:
            async with async_session() as session:
                async with session.begin():
                    now = datetime.now()
                    two_hours_ago = now - timedelta(hours=2)
                    # Получаем все user_queries, которые не удалены и старше 2 часов
                    result = await session.execute(
                        UserQueries.__table__.select().where(
                            UserQueries.query_created_at <= two_hours_ago,
                            UserQueries.deleted_at.is_(None)
                        )
                    )
                    old_queries = result.fetchall()
                    for row in old_queries:
                        query_id = row.query_id
                        logging.info(f"Очищаю данные для запроса {query_id}")
                        await UserQueriesDAO.delete_query_by_id(query_id, session)
                    await session.commit()

        except Exception as e:
            logging.error(f"Ошибка при очистке старых запросов: {e}")
            raise e
        await asyncio.sleep(300)  # 5 минут

if __name__ == "__main__":
    asyncio.run(cleanup_old_queries())
