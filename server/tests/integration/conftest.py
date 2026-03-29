from unittest.mock import MagicMock, AsyncMock

import pytest
import pytest_asyncio
import httpx
from httpx import ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

from server.api.database.database import get_db


@pytest.fixture
def mock_db():
    """Замена AsyncSession для интеграционных тестов."""
    db = AsyncMock(spec=AsyncSession)

    result = MagicMock()
    result.scalars.return_value.first.return_value = None
    result.scalars.return_value.one_or_none.return_value = None
    result.scalars.return_value.all.return_value = []
    result.scalar_one_or_none.return_value = None
    result.scalar.return_value = None
    result.fetchall.return_value = []
    result.all.return_value = []

    db.execute.return_value = result
    db.commit = AsyncMock()
    db.rollback = AsyncMock()
    db.flush = AsyncMock()
    db.add = MagicMock()
    db.scalar = AsyncMock(return_value=None)

    return db


@pytest.fixture
def mock_authorize():
    """Замена AuthJWT: jwt_required не бросает исключений, user_id = 1."""
    auth = MagicMock()
    auth.jwt_required = MagicMock()
    auth.jwt_refresh_token_required = MagicMock()
    auth.get_jwt_subject = MagicMock(return_value="1")
    auth.create_access_token = MagicMock(return_value="fake-access-token")
    auth.create_refresh_token = MagicMock(return_value="fake-refresh-token")
    auth.set_access_cookies = MagicMock()
    auth.set_refresh_cookies = MagicMock()
    auth.unset_jwt_cookies = MagicMock()
    return auth


@pytest.fixture
def app_fixture(mock_db, mock_authorize):
    """FastAPI app с переопределёнными зависимостями get_db и AuthJWT."""
    from fastapi_jwt_auth import AuthJWT

    from server.__main__ import app

    app.dependency_overrides[get_db] = lambda: mock_db
    app.dependency_overrides[AuthJWT] = lambda: mock_authorize

    yield app

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client(app_fixture):
    """httpx.AsyncClient для интеграционных HTTP-тестов."""
    async with httpx.AsyncClient(
        transport=ASGITransport(app=app_fixture),
        base_url="http://test",
    ) as client:
        yield client
