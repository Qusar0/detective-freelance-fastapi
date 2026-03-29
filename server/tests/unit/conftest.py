import pytest
from unittest.mock import MagicMock, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture
def mock_db():
    """Замена AsyncSession для unit-тестов без реального подключения к БД."""
    db = AsyncMock(spec=AsyncSession)

    result = MagicMock()
    result.scalars.return_value.first.return_value = None
    result.scalars.return_value.one_or_none.return_value = None
    result.scalars.return_value.all.return_value = []
    result.scalar_one_or_none.return_value = None
    result.scalar.return_value = None
    result.fetchall.return_value = []

    db.execute.return_value = result
    db.commit = AsyncMock()
    db.rollback = AsyncMock()
    db.flush = AsyncMock()
    db.add = MagicMock()
    db.scalar = AsyncMock(return_value=None)

    return db
