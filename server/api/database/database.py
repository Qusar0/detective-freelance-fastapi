from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from server.api.conf.config import settings


engine = create_async_engine(
    settings.database_url,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=1800,
    connect_args={
        "server_settings": {
            "tcp_keepalives_idle": "60",
            "tcp_keepalives_interval": "10",
            "tcp_keepalives_count": "5",
        }
    },
)

async_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db():
    async with async_session() as session:
        yield session
