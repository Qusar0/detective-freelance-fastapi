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
    async with async_session() as session:
        yield session
