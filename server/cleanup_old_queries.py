# Скрипт для периодической очистки данных старых запросов
import asyncio
from datetime import datetime, timedelta
from server.api.database.database import async_session
from server.api.dao.user_queries import UserQueriesDAO
from server.api.models.models import UserQueries
from sqlalchemy import select
from loguru import logger
import server.api.models.irbis_models  # noqa: F401


async def cleanup_old_queries():
    while True:
        try:
            async with async_session() as session:
                async with session.begin():
                    now = datetime.now()
                    two_hours_ago = now - timedelta(hours=2)

                    result = await session.execute(
                        select(UserQueries).where(
                            UserQueries.query_created_at <= two_hours_ago,
                            UserQueries.deleted_at.is_(None)
                        )
                    )
                    old_queries = result.scalars().all()
                    for query in old_queries:
                        logger.info(f"Очищаю данные для запроса {query.query_id}")
                        await UserQueriesDAO.delete_query_info_by_id(query.query_id, session)
        except Exception as e:
            logger.error(f"Ошибка при очистке старых запросов: {e}")
        logger.info("Спим 5 минут")
        await asyncio.sleep(300)

if __name__ == "__main__":
    asyncio.run(cleanup_old_queries())
