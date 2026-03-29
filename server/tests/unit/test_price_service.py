from unittest.mock import AsyncMock, patch

import pytest

from server.api.services.price import (
    calculate_email_price,
    calculate_name_price,
    calculate_num_price,
)


def test_num_price_mentions_only():
    """Только mentions - цена 5."""
    assert calculate_num_price(["mentions"]) == 5


def test_num_price_tags_only():
    """Только tags - цена 20."""
    assert calculate_num_price(["tags"]) == 20


def test_num_price_both():
    """mentions + tags - цена 25."""
    assert calculate_num_price(["mentions", "tags"]) == 25


def test_num_price_empty():
    """Пустой список методов - цена 0."""
    assert calculate_num_price([]) == 0


def test_num_price_unknown_type():
    """Неизвестный тип метода - цена 0."""
    assert calculate_num_price(["unknown"]) == 0


def test_email_price_mentions_only():
    """Только mentions - цена 5."""
    assert calculate_email_price(["mentions"]) == 5


def test_email_price_acc_search_only():
    """Только acc search - цена 120."""
    assert calculate_email_price(["acc search"]) == 120


def test_email_price_both():
    """mentions + acc search - цена 125."""
    assert calculate_email_price(["mentions", "acc search"]) == 125


def test_email_price_empty():
    """Пустой список методов - цена 0."""
    assert calculate_email_price([]) == 0


@pytest.mark.asyncio
async def test_name_price_no_patronymic_no_keywords(mock_db):
    """
    Без отчества, без ключевых слов, 0 дефолтных из БД.
    Формула: fi_queries = 2*5=10; query_count = 10*1=10; price = (10*0.02)*3 = 0.6
    """
    with patch(
        "server.api.services.price.KeywordsDAO.get_default_keywords",
        new=AsyncMock(return_value=(0, {})),
    ):
        price = await calculate_name_price(
            db=mock_db,
            search_patronymic="",
            keywords=[],
            default_keywords_type="reputation",
            languages=["ru"],
        )
    assert price == 0.6


@pytest.mark.asyncio
async def test_name_price_with_patronymic_and_keywords(mock_db):
    """
    С отчеством, 2 пользовательских слова, 3 дефолтных из БД, 1 язык.
    Формула: len_all=5; fio_queries=4*5=20; not_to_search=10*3=30;
             query_count=20*5-30=70; price=(70*0.02)*3=4.2
    """
    with patch(
        "server.api.services.price.KeywordsDAO.get_default_keywords",
        new=AsyncMock(return_value=(3, {})),
    ):
        price = await calculate_name_price(
            db=mock_db,
            search_patronymic="Иванович",
            keywords=["word1", "word2"],
            default_keywords_type="reputation",
            languages=["ru"],
        )
    assert price == 4.2


@pytest.mark.asyncio
async def test_name_price_returns_rounded(mock_db):
    """Результат округляется до 2 знаков после запятой."""
    with patch(
        "server.api.services.price.KeywordsDAO.get_default_keywords",
        new=AsyncMock(return_value=(0, {})),
    ):
        price = await calculate_name_price(
            db=mock_db,
            search_patronymic="",
            keywords=[],
            default_keywords_type="reputation",
            languages=["ru"],
        )
    assert price == round(price, 2)


@pytest.mark.asyncio
async def test_name_price_calls_keywords_dao_once(mock_db):
    """KeywordsDAO.get_default_keywords вызывается ровно один раз."""
    mock_get = AsyncMock(return_value=(0, {}))
    with patch("server.api.services.price.KeywordsDAO.get_default_keywords", new=mock_get):
        await calculate_name_price(
            db=mock_db,
            search_patronymic="",
            keywords=[],
            default_keywords_type="reputation",
            languages=["ru"],
        )
    mock_get.assert_called_once()
