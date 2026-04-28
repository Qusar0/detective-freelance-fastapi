from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from passlib.hash import bcrypt

from server.tests.helpers.factories import make_user, make_user_balance, make_event


@pytest.mark.asyncio
async def test_is_authenticated_with_valid_jwt(client, mock_authorize):
    """Авторизованный пользователь получает статус 200."""
    response = await client.get("/api/users/is_authenticated")
    assert response.status_code == 200
    assert response.json()["status"] == "success"


@pytest.mark.asyncio
async def test_is_authenticated_without_jwt(client, mock_authorize):
    """Запрос без токена возвращает 401."""
    from fastapi_jwt_auth.exceptions import MissingTokenError
    mock_authorize.jwt_required.side_effect = MissingTokenError(
        status_code=401, message="Missing JWT"
    )
    response = await client.get("/api/users/is_authenticated")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_balance_returns_float(client, mock_db):
    """Баланс пользователя возвращается как число с плавающей точкой."""
    balance = make_user_balance(user_id=1, balance=150.5)
    mock_db.execute.return_value.scalar_one_or_none.return_value = balance

    response = await client.get("/api/users/get_balance")

    assert response.status_code == 200
    assert response.json() == 150.5


@pytest.mark.asyncio
async def test_get_balance_not_found(client, mock_db):
    """Если баланс не найден в БД, возвращается 404."""
    mock_db.execute.return_value.scalar_one_or_none.return_value = None

    response = await client.get("/api/users/get_balance")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_events_returns_dict(client, mock_db):
    """Список событий возвращается как словарь с числовыми ключами."""
    events = [make_event(event_id=i, query_id=1) for i in range(3)]
    mock_db.execute.return_value.scalars.return_value.all.return_value = events

    response = await client.get("/api/users/get_events")

    assert response.status_code == 200
    data = response.json()
    assert "0" in data
    assert "1" in data
    assert "2" in data


@pytest.mark.asyncio
async def test_get_events_empty(client, mock_db):
    """Если событий нет, возвращается пустой словарь."""
    mock_db.execute.return_value.scalars.return_value.all.return_value = []

    response = await client.get("/api/users/get_events")

    assert response.status_code == 200
    assert response.json() == {}


@pytest.mark.asyncio
async def test_change_event_status_success(client, mock_db):
    """Существующее событие помечается как seen, статус 200."""
    event = make_event(event_id=5)
    mock_db.execute.return_value.scalar_one_or_none.return_value = event

    response = await client.post(
        "/api/users/change_event_status",
        json={"event_id": 5},
    )

    assert response.status_code == 200
    assert event.event_status == "seen"
    mock_db.commit.assert_called()


@pytest.mark.asyncio
async def test_change_event_status_not_found(client, mock_db):
    """Событие не найдено: статус 404."""
    mock_db.execute.return_value.scalar_one_or_none.return_value = None

    response = await client.post(
        "/api/users/change_event_status",
        json={"event_id": 999},
    )
    assert response.status_code == 404


@pytest.fixture
def top_up_payload():
    """Типичный payload для пополнения баланса."""
    return {
        "transaction_id": 123456,
        "currency": "RUB",
        "payment_amount": 500.0,
        "operation_type": "Payment",
        "invoice_id": 789,
        "account_id": 1,
        "email": "user@example.com",
        "date_time": "2025-01-01T12:00:00",
        "ip_address": "127.0.0.1",
        "status": "Completed",
    }


@pytest.mark.asyncio
async def test_top_up_balance_completed(client, mock_db, top_up_payload):
    """Статус Completed: баланс увеличивается, ответ 200."""
    user = make_user(is_confirmed=True)
    balance = make_user_balance(user_id=1, balance=100.0)

    call_count = 0

    async def fake_execute(stmt, *args, **kwargs):
        nonlocal call_count
        result = MagicMock()
        result.scalar_one_or_none.return_value = None
        result.scalars.return_value.first.return_value = None
        if call_count == 0:
            result.scalar_one_or_none.return_value = user
        elif call_count == 1:
            result.scalar_one_or_none.return_value = balance
        call_count += 1
        return result

    mock_db.execute = fake_execute

    with patch("server.api.routers.users.publish_event", new=AsyncMock()):
        with patch("server.api.routers.users.generate_sse_message_type", new=AsyncMock(return_value="ch")):
            response = await client.post("/api/users/top_up_balance", json=top_up_payload)

    assert response.status_code == 200
    assert balance.balance == 600.0


@pytest.mark.asyncio
async def test_top_up_balance_user_not_confirmed(client, mock_db, top_up_payload):
    """Неподтверждённый пользователь получает 403."""
    user = make_user(is_confirmed=False)
    mock_db.execute.return_value.scalar_one_or_none.return_value = user

    with patch("server.api.routers.users.send_confirmation_email", new=AsyncMock()):
        response = await client.post("/api/users/top_up_balance", json=top_up_payload)

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_top_up_balance_user_not_found(client, mock_db, top_up_payload):
    """Пользователь не найден: статус 404."""
    mock_db.execute.return_value.scalar_one_or_none.return_value = None

    response = await client.post("/api/users/top_up_balance", json=top_up_payload)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_change_password_success(client, mock_db):
    """Верный старый пароль: пароль обновляется, send_email вызывается, статус 200."""
    user = make_user(password_plain="oldpassword1")
    mock_db.execute.return_value.scalar_one_or_none.return_value = user

    with patch("server.api.routers.users.send_email", new=AsyncMock()) as mock_send:
        response = await client.post(
            "/api/users/change_password",
            json={"old_password": "oldpassword1", "new_password": "newpassword1"},
        )

    assert response.status_code == 200
    mock_send.assert_called_once()
    assert not bcrypt.verify("oldpassword1", user.password)


@pytest.mark.asyncio
async def test_change_password_wrong_old_password(client, mock_db):
    """Неверный старый пароль: статус 403."""
    user = make_user(password_plain="correct_password")
    mock_db.execute.return_value.scalar_one_or_none.return_value = user

    response = await client.post(
        "/api/users/change_password",
        json={"old_password": "wrong_password", "new_password": "newpassword1"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_change_password_user_not_found(client, mock_db):
    """Пользователь не найден: статус 404."""
    mock_db.execute.return_value.scalar_one_or_none.return_value = None

    response = await client.post(
        "/api/users/change_password",
        json={"old_password": "oldpassword1", "new_password": "newpassword1"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_default_language(client):
    """UserLanguageDAO возвращает код языка, роутер отдаёт его в ответе."""
    with patch(
        "server.api.routers.users.UserLanguageDAO.get_user_default_language",
        new=AsyncMock(return_value="ru"),
    ):
        response = await client.get("/api/users/default_language")

    assert response.status_code == 200
    assert response.json()["default_language_code"] == "ru"


@pytest.mark.asyncio
async def test_get_default_language_unauthenticated(client, mock_authorize):
    """Без токена возвращается 401."""
    from fastapi_jwt_auth.exceptions import MissingTokenError
    mock_authorize.jwt_required.side_effect = MissingTokenError(
        status_code=401, message="Missing JWT"
    )
    response = await client.get("/api/users/default_language")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_set_default_language_success(client):
    """DAO возвращает True: язык обновляется, статус 200."""
    with patch(
        "server.api.routers.users.UserLanguageDAO.set_user_default_language",
        new=AsyncMock(return_value=True),
    ):
        response = await client.post(
            "/api/users/set_default_language",
            json={"default_language_code": "en"},
        )

    assert response.status_code == 200
    assert response.json()["default_language_code"] == "en"


@pytest.mark.asyncio
async def test_set_default_language_not_found(client):
    """DAO возвращает False: язык не найден, статус 400."""
    with patch(
        "server.api.routers.users.UserLanguageDAO.set_user_default_language",
        new=AsyncMock(return_value=False),
    ):
        response = await client.post(
            "/api/users/set_default_language",
            json={"default_language_code": "xx"},
        )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_balance_history_pagination(client):
    """История баланса с пагинацией возвращает корректный BalanceHistoryResponse."""
    fake_result = {
        "items": [],
        "total": 0,
        "page": 0,
        "size": 10,
        "total_pages": 0,
    }
    with patch(
        "server.api.routers.users.UserBalanceHistoryDAO.get_user_history",
        new=AsyncMock(return_value=fake_result),
    ):
        response = await client.get("/api/users/balance_history?page=0&size=10")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["size"] == 10


@pytest.mark.asyncio
async def test_balance_history_invalid_size(client):
    """size=0 нарушает ограничение ge=1, Pydantic возвращает 422."""
    response = await client.get("/api/users/balance_history?size=0")
    assert response.status_code == 422
