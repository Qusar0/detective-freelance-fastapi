from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from server.api.conf.config import settings


engine = create_async_engine(settings.database_url, echo=True)

async_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db():
    """Асинхронный генератор для получения сессии базы данных.
    
    Используется как dependency в FastAPI для внедрения сессии БД
    в обработчики запросов.
    
    Yields:
        AsyncSession: Асинхронная сессия SQLAlchemy для работы с БД
    """
    async with async_session() as session:
        yield session
