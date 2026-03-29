from unittest.mock import AsyncMock, MagicMock

import pytest

from server.tests.helpers.factories import make_user_query

_QUERY_MODULE = "server.api.routers.query"

_FIND_BY_NAME_PAYLOAD = {
    "search_name": "Иван",
    "search_surname": "Иванов",
    "search_patronymic": "",
    "search_plus": "",
    "search_minus": "",
    "keywords": [],
    "default_keywords_type": "reputation",
    "search_engines": ["google"],
    "languages": ["ru"],
}

_TRANSLATED_NAME_FIELDS = {
    "name": {"ru": "Иван"}, "surname": {"ru": "Иванов"},
    "patronymic": {"ru": ""}, "plus": {"ru": ""},
    "minus": {"ru": ""}, "keywords": {"ru": []},
}


@pytest.mark.asyncio
async def test_delete_query_success(client, mocker):
    """Запрос найден: удаляется, возвращается 200."""
    query = make_user_query(query_id=1, user_id=1)
    mocker.patch(f"{_QUERY_MODULE}.UserQueriesDAO.get_query_by_id", new=AsyncMock(return_value=query))
    mock_delete = mocker.patch(f"{_QUERY_MODULE}.UserQueriesDAO.delete_query_info_by_id", new=AsyncMock())

    response = await client.post("/api/queries/delete_query?query_id=1")

    assert response.status_code == 200
    assert response.json()["message"] == "Success"
    mock_delete.assert_called_once()


@pytest.mark.asyncio
async def test_delete_query_not_found(client, mocker):
    """Запрос не найден или не принадлежит пользователю: 404."""
    mocker.patch(f"{_QUERY_MODULE}.UserQueriesDAO.get_query_by_id", new=AsyncMock(return_value=None))

    response = await client.post("/api/queries/delete_query?query_id=999")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_query_unauthenticated(client, mock_authorize):
    """Без токена возвращается 401."""
    from fastapi_jwt_auth.exceptions import MissingTokenError
    mock_authorize.jwt_required.side_effect = MissingTokenError(status_code=401, message="Missing JWT")

    response = await client.post("/api/queries/delete_query?query_id=1")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_queries_count(client, mock_db):
    """Возвращает количество запросов по категории."""
    mock_db.execute.return_value.fetchall.return_value = [MagicMock()] * 3

    response = await client.get("/api/queries/queries_count?query_category=name")

    assert response.status_code == 200
    assert response.json()["count"] == 3


@pytest.mark.asyncio
async def test_find_by_name_success(client, mocker):
    """Успешный поиск по имени: Celery-задача запускается, статус 200."""
    mocker.patch(f"{_QUERY_MODULE}.translate_name_fields", new=AsyncMock(return_value=_TRANSLATED_NAME_FIELDS))
    mocker.patch(f"{_QUERY_MODULE}.calculate_name_price", new=AsyncMock(return_value=5.0))
    mocker.patch(f"{_QUERY_MODULE}.UserQueriesDAO.save_user_query", new=AsyncMock(return_value=1))
    mocker.patch(f"{_QUERY_MODULE}.UserBalancesDAO.subtract_balance", new=AsyncMock())
    mocker.patch(f"{_QUERY_MODULE}.BalanceHistoryDAO.save_payment_to_history", new=AsyncMock())
    mocker.patch(f"{_QUERY_MODULE}.QueriesBalanceDAO.save_query_balance", new=AsyncMock())
    mocker.patch(f"{_QUERY_MODULE}.generate_sse_message_type", new=AsyncMock(return_value="channel"))
    mock_task = mocker.patch(f"{_QUERY_MODULE}.start_search_by_name")
    mock_task.apply_async = MagicMock()

    response = await client.post("/api/queries/find_by_name", json=_FIND_BY_NAME_PAYLOAD)

    assert response.status_code == 200
    mock_task.apply_async.assert_called_once()


@pytest.mark.asyncio
async def test_find_by_name_insufficient_balance(client, mocker):
    """Недостаточно средств: возвращается 400."""
    from server.api.dao.user_balances import InsufficientFundsError

    mocker.patch(f"{_QUERY_MODULE}.translate_name_fields", new=AsyncMock(return_value=_TRANSLATED_NAME_FIELDS))
    mocker.patch(f"{_QUERY_MODULE}.calculate_name_price", new=AsyncMock(return_value=5.0))
    mocker.patch(f"{_QUERY_MODULE}.UserQueriesDAO.save_user_query", new=AsyncMock(return_value=1))
    mocker.patch(f"{_QUERY_MODULE}.generate_sse_message_type", new=AsyncMock(return_value="channel"))
    mocker.patch(
        f"{_QUERY_MODULE}.UserBalancesDAO.subtract_balance",
        new=AsyncMock(side_effect=InsufficientFundsError(current_balance=0.0, required_amount=5.0)),
    )

    response = await client.post("/api/queries/find_by_name", json=_FIND_BY_NAME_PAYLOAD)

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_find_by_name_unauthenticated(client, mock_authorize):
    """Без токена возвращается 401."""
    from fastapi_jwt_auth.exceptions import MissingTokenError
    mock_authorize.jwt_required.side_effect = MissingTokenError(status_code=401, message="Missing JWT")

    response = await client.post("/api/queries/find_by_name", json=_FIND_BY_NAME_PAYLOAD)

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_find_by_number_success(client, mocker):
    """Успешный поиск по номеру: Celery-задача запускается, статус 200."""
    mocker.patch(f"{_QUERY_MODULE}.UserQueriesDAO.save_user_query", new=AsyncMock(return_value=1))
    mocker.patch(f"{_QUERY_MODULE}.UserBalancesDAO.subtract_balance", new=AsyncMock())
    mocker.patch(f"{_QUERY_MODULE}.BalanceHistoryDAO.save_payment_to_history", new=AsyncMock())
    mocker.patch(f"{_QUERY_MODULE}.QueriesBalanceDAO.save_query_balance", new=AsyncMock())
    mocker.patch(f"{_QUERY_MODULE}.generate_sse_message_type", new=AsyncMock(return_value="channel"))
    mock_task = mocker.patch(f"{_QUERY_MODULE}.start_search_by_num")
    mock_task.apply_async = MagicMock()

    response = await client.post(
        "/api/queries/find_by_number",
        json={"search_number": "+79001234567", "methods_type": ["mentions"]},
    )

    assert response.status_code == 200
    mock_task.apply_async.assert_called_once()


@pytest.mark.asyncio
async def test_calculate_price_returns_price(client, mocker):
    """calculate_price возвращает {"price": X}."""
    mocker.patch(f"{_QUERY_MODULE}.calculate_name_price", new=AsyncMock(return_value=3.6))

    response = await client.post(
        "/api/queries/calculate_price",
        json={
            "search_patronymic": "",
            "keywords": [],
            "default_keywords_type": "reputation",
            "languages": ["ru"],
        },
    )

    assert response.status_code == 200
    assert response.json()["price"] == 3.6
