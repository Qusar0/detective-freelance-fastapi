from unittest.mock import AsyncMock, patch
from email.message import EmailMessage

import pytest
from freezegun import freeze_time

from server.api.services.mail import (
    confirm_token,
    generate_conformation_token,
    send_email,
)


def test_token_roundtrip():
    """Генерируем токен и тут же подтверждаем - должны получить исходный email."""
    token = generate_conformation_token("user@example.com")
    result = confirm_token(token)
    assert result == "user@example.com"


def test_token_invalid_returns_false():
    """Невалидный токен возвращает False."""
    result = confirm_token("this-is-not-a-valid-token")
    assert result is False


def test_token_expired_returns_false():
    """Токен, сгенерированный в прошлом, с expiration=0 считается истёкшим."""
    with freeze_time("2025-01-01 00:00:00"):
        token = generate_conformation_token("user@example.com")

    result = confirm_token(token, expiration=0)
    assert result is False


def test_token_tampered_returns_false():
    """Испорченный токен не проходит валидацию."""
    token = generate_conformation_token("user@example.com")
    bad_token = token[:-1] + ("A" if token[-1] != "A" else "B")
    assert confirm_token(bad_token) is False


@pytest.mark.asyncio
async def test_send_email_calls_aiosmtplib():
    """aiosmtplib.send вызывается с правильными параметрами SMTP-сервера."""
    with patch("server.api.services.mail.send", new=AsyncMock()) as mock_send:
        await send_email(
            subject="Test Subject",
            recipients=["recipient@example.com"],
            body="Hello body",
        )
    mock_send.assert_called_once()
    _, kwargs = mock_send.call_args
    assert kwargs["hostname"] == "smtp.test.com"
    assert kwargs["port"] == 587


@pytest.mark.asyncio
async def test_send_email_sets_headers():
    """Subject и адреса получателей устанавливаются корректно."""
    captured: list[EmailMessage] = []

    async def fake_send(message, **kwargs):
        captured.append(message)

    with patch("server.api.services.mail.send", new=fake_send):
        await send_email(
            subject="Тема письма",
            recipients=["a@example.com", "b@example.com"],
            body="Текст письма",
        )

    msg = captured[0]
    assert msg["Subject"] == "Тема письма"
    assert "a@example.com" in msg["To"]
    assert "b@example.com" in msg["To"]


@pytest.mark.asyncio
async def test_send_email_with_html_calls_add_alternative():
    """При передаче html-параметра вызывается add_alternative."""
    with patch("server.api.services.mail.send", new=AsyncMock()):
        with patch.object(EmailMessage, "add_alternative") as mock_alt:
            await send_email(
                subject="S",
                recipients=["r@example.com"],
                body="plain",
                html="<b>html</b>",
            )
    mock_alt.assert_called_once_with("<b>html</b>", subtype="html")


@pytest.mark.asyncio
async def test_send_email_without_html_skips_add_alternative():
    """Без html-параметра add_alternative не вызывается."""
    with patch("server.api.services.mail.send", new=AsyncMock()):
        with patch.object(EmailMessage, "add_alternative") as mock_alt:
            await send_email(
                subject="S",
                recipients=["r@example.com"],
                body="plain",
            )
    mock_alt.assert_not_called()
