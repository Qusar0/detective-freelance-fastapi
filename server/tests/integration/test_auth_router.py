from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from server.api.services.mail import generate_conformation_token
from server.tests.helpers.factories import make_user


@pytest.mark.asyncio
async def test_register_new_user_success(client, mock_db):
    """Новый пользователь регистрируется: send_email вызывается, статус 200."""
    role_mock = MagicMock()
    role_mock.id = 1
    mock_db.scalar.return_value = role_mock

    with patch("server.api.routers.auth.send_email", new=AsyncMock()) as mock_send:
        response = await client.post(
            "/api/v1/auth/register",
            json={"email": "newuser@example.com", "password": "password123"},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    mock_send.assert_called_once()


@pytest.mark.asyncio
async def test_register_existing_user_sends_already_registered_email(client, mock_db):
    """Существующий пользователь: send_email вызывается с уже-зарегистрированным контентом."""
    existing = make_user(email="existing@example.com")
    mock_db.execute.return_value.scalars.return_value.first.return_value = existing

    with patch("server.api.routers.auth.send_email", new=AsyncMock()) as mock_send:
        response = await client.post(
            "/api/v1/auth/register",
            json={"email": "existing@example.com", "password": "password123"},
        )

    assert response.status_code == 200
    mock_send.assert_called_once()


@pytest.mark.asyncio
async def test_register_invalid_email_returns_422(client):
    """Невалидный email вызывает ошибку валидации Pydantic (422)."""
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "not-an-email", "password": "password123"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_success(client, mock_db, mock_authorize):
    """Верный пароль: ответ 200, cookies access и refresh установлены."""
    user = make_user(email="user@example.com", password_plain="password123")
    mock_db.execute.return_value.scalars.return_value.first.return_value = user

    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "user@example.com", "password": "password123"},
    )

    assert response.status_code == 200
    mock_authorize.set_access_cookies.assert_called_once()
    mock_authorize.set_refresh_cookies.assert_called_once()


@pytest.mark.asyncio
async def test_login_wrong_password(client, mock_db):
    """Неверный пароль: статус 422."""
    user = make_user(email="user@example.com", password_plain="correct_password")
    mock_db.execute.return_value.scalars.return_value.first.return_value = user

    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "user@example.com", "password": "wrong_password"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_user_not_found(client, mock_db):
    """Пользователь не найден: статус 422."""
    mock_db.execute.return_value.scalars.return_value.first.return_value = None

    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "unknown@example.com", "password": "password123"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_confirm_valid_token_confirms_user(client, mock_db):
    """Валидный токен подтверждает пользователя: is_confirmed=True, commit вызван."""
    user = make_user(email="user@example.com", is_confirmed=False)
    mock_db.execute.return_value.scalars.return_value.first.return_value = user

    token = generate_conformation_token("user@example.com")
    response = await client.get(f"/api/v1/auth/confirm/{token}")

    assert response.status_code == 200
    assert user.is_confirmed is True
    mock_db.commit.assert_called()


@pytest.mark.asyncio
async def test_confirm_already_confirmed(client, mock_db):
    """Уже подтверждённый пользователь: статус 200, сообщение об этом."""
    user = make_user(email="user@example.com", is_confirmed=True)
    mock_db.execute.return_value.scalars.return_value.first.return_value = user

    token = generate_conformation_token("user@example.com")
    response = await client.get(f"/api/v1/auth/confirm/{token}")

    assert response.status_code == 200
    assert "already confirmed" in response.json()["message"]


@pytest.mark.asyncio
async def test_confirm_invalid_token(client):
    """Невалидный токен возвращает 400."""
    response = await client.get("/api/v1/auth/confirm/invalid-token-here")
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_confirm_user_not_found(client, mock_db):
    """Токен валиден, но пользователь в БД не найден - 404."""
    mock_db.execute.return_value.scalars.return_value.first.return_value = None

    token = generate_conformation_token("ghost@example.com")
    response = await client.get(f"/api/v1/auth/confirm/{token}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_forgot_password_user_exists(client, mock_db):
    """Пользователь найден: send_email вызывается, статус 200."""
    user = make_user(email="user@example.com")
    mock_db.execute.return_value.scalars.return_value.first.return_value = user

    with patch("server.api.routers.auth.send_email", new=AsyncMock()) as mock_send:
        response = await client.post(
            "/api/v1/auth/forgot_password",
            params={"email": "user@example.com"},
        )

    assert response.status_code == 200
    mock_send.assert_called_once()


@pytest.mark.asyncio
async def test_forgot_password_user_not_found(client, mock_db):
    """Пользователь не найден: статус 200, send_email не вызывается."""
    mock_db.execute.return_value.scalars.return_value.first.return_value = None

    with patch("server.api.routers.auth.send_email", new=AsyncMock()) as mock_send:
        response = await client.post(
            "/api/v1/auth/forgot_password",
            params={"email": "unknown@example.com"},
        )

    assert response.status_code == 200
    mock_send.assert_not_called()


@pytest.mark.asyncio
async def test_reset_password_success(client, mock_db):
    """Валидный токен + существующий пользователь: пароль обновляется, статус 200."""
    user = make_user(email="user@example.com")
    mock_db.execute.return_value.scalars.return_value.first.return_value = user

    token = generate_conformation_token("user@example.com")
    old_password_hash = user.password

    response = await client.post(
        "/api/v1/auth/reset_password",
        json={"token": token, "new_password": "newpassword123"},
    )

    assert response.status_code == 200
    assert user.password != old_password_hash


@pytest.mark.asyncio
async def test_reset_password_invalid_token(client):
    """Невалидный токен: статус 400."""
    response = await client.post(
        "/api/v1/auth/reset_password",
        json={"token": "bad-token", "new_password": "newpassword123"},
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_reset_password_user_not_found(client, mock_db):
    """Токен валиден, но пользователь не найден: статус 404."""
    mock_db.execute.return_value.scalars.return_value.first.return_value = None

    token = generate_conformation_token("ghost@example.com")
    response = await client.post(
        "/api/v1/auth/reset_password",
        json={"token": token, "new_password": "newpassword123"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_logout_unsets_cookies(client, mock_authorize):
    """Logout очищает JWT-cookies через unset_jwt_cookies."""
    response = await client.post("/api/v1/auth/logout")
    assert response.status_code == 200
    mock_authorize.unset_jwt_cookies.assert_called_once()
