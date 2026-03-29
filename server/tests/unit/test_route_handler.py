import pytest
from fastapi import HTTPException
from fastapi_jwt_auth.exceptions import MissingTokenError

from server.api.utils.route_handler import handle_route_errors
from server.api.dao.user_balances import InsufficientFundsError


def _wrap(fn):
    """Оборачивает асинхронную функцию декоратором handle_route_errors."""
    return handle_route_errors("Тестовая ошибка")(fn)


@pytest.mark.asyncio
async def test_returns_result_on_success():
    """Декоратор прозрачно возвращает результат успешной функции."""
    @_wrap
    async def handler():
        return {"ok": True}

    result = await handler()
    assert result == {"ok": True}


@pytest.mark.asyncio
async def test_reraises_http_exception():
    """HTTPException пробрасывается без изменений статуса и детали."""
    @_wrap
    async def handler():
        raise HTTPException(status_code=404, detail="не найдено")

    with pytest.raises(HTTPException) as exc_info:
        await handler()
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "не найдено"


@pytest.mark.asyncio
async def test_converts_missing_token_to_401():
    """MissingTokenError преобразуется в HTTPException 401."""
    @_wrap
    async def handler():
        raise MissingTokenError(status_code=401, message="Missing JWT")

    with pytest.raises(HTTPException) as exc_info:
        await handler()
    assert exc_info.value.status_code == 401


@pytest.mark.asyncio
async def test_converts_insufficient_funds_to_400():
    """InsufficientFundsError преобразуется в HTTPException 400."""
    @_wrap
    async def handler():
        raise InsufficientFundsError(current_balance=5.0, required_amount=100.0)

    with pytest.raises(HTTPException) as exc_info:
        await handler()
    assert exc_info.value.status_code == 400


@pytest.mark.asyncio
async def test_converts_generic_exception_to_500():
    """Произвольное исключение преобразуется в HTTPException 500."""
    @_wrap
    async def handler():
        raise ValueError("что-то сломалось")

    with pytest.raises(HTTPException) as exc_info:
        await handler()
    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Внутренняя ошибка сервера"
