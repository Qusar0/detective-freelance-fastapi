from unittest.mock import AsyncMock, MagicMock, patch
from contextlib import asynccontextmanager

import pytest
from botocore.exceptions import ClientError
from fastapi import HTTPException

from server.api.services.file_storage import FileStorageService


def _make_client_error(code: str) -> ClientError:
    """Создаёт ClientError с заданным кодом ошибки."""
    return ClientError({"Error": {"Code": code, "Message": "test"}}, "operation")


def _make_storage() -> FileStorageService:
    """Создаёт экземпляр FileStorageService с тестовыми параметрами."""
    return FileStorageService(
        endpoint="http://minio:9000",
        access_key="testkey",
        secret_key="testsecret",
        bucket="test-bucket",
    )


def _make_s3_context(client_mock: MagicMock):
    """Создаёт асинхронный контекстный менеджер, возвращающий client_mock."""
    @asynccontextmanager
    async def ctx(*args, **kwargs):
        yield client_mock

    return ctx


@pytest.mark.asyncio
async def test_save_query_data_returns_key():
    """При успешной загрузке возвращает ключ вида query_{id}.html."""
    client = MagicMock()
    client.create_bucket = AsyncMock()
    client.put_object = AsyncMock()

    storage = _make_storage()
    with patch.object(storage._session, "client", _make_s3_context(client)):
        key = await storage.save_query_data(query_id=42, data="<html/>")

    assert key == "query_42.html"


@pytest.mark.asyncio
async def test_save_query_data_ignores_bucket_already_owned():
    """BucketAlreadyOwnedByYou не прерывает загрузку."""
    client = MagicMock()
    client.create_bucket = AsyncMock(
        side_effect=_make_client_error("BucketAlreadyOwnedByYou")
    )
    client.put_object = AsyncMock()

    storage = _make_storage()
    with patch.object(storage._session, "client", _make_s3_context(client)):
        key = await storage.save_query_data(query_id=1, data="data")

    assert key == "query_1.html"
    client.put_object.assert_called_once()


@pytest.mark.asyncio
async def test_save_query_data_raises_500_on_s3_error():
    """Другой ClientError приводит к HTTPException 500."""
    client = MagicMock()
    client.create_bucket = AsyncMock(side_effect=_make_client_error("AccessDenied"))
    client.put_object = AsyncMock()

    storage = _make_storage()
    with patch.object(storage._session, "client", _make_s3_context(client)):
        with pytest.raises(HTTPException) as exc_info:
            await storage.save_query_data(query_id=1, data="data")

    assert exc_info.value.status_code == 500


@pytest.mark.asyncio
async def test_get_query_data_returns_content():
    """Успешное чтение возвращает декодированную строку."""
    body_mock = AsyncMock()
    body_mock.__aenter__ = AsyncMock(return_value=body_mock)
    body_mock.__aexit__ = AsyncMock(return_value=False)
    body_mock.read = AsyncMock(return_value=b"hello world")

    client = MagicMock()
    client.get_object = AsyncMock(return_value={"Body": body_mock})

    storage = _make_storage()
    with patch.object(storage._session, "client", _make_s3_context(client)):
        result = await storage.get_query_data("query_1.html")

    assert result == "hello world"


@pytest.mark.asyncio
async def test_get_query_data_raises_404_on_no_such_key():
    """NoSuchKey приводит к HTTPException 404."""
    client = MagicMock()
    client.get_object = AsyncMock(side_effect=_make_client_error("NoSuchKey"))

    storage = _make_storage()
    with patch.object(storage._session, "client", _make_s3_context(client)):
        with pytest.raises(HTTPException) as exc_info:
            await storage.get_query_data("missing.html")

    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_get_query_data_raises_500_on_other_error():
    """Другой ClientError приводит к HTTPException 500."""
    client = MagicMock()
    client.get_object = AsyncMock(side_effect=_make_client_error("InternalError"))

    storage = _make_storage()
    with patch.object(storage._session, "client", _make_s3_context(client)):
        with pytest.raises(HTTPException) as exc_info:
            await storage.get_query_data("file.html")

    assert exc_info.value.status_code == 500


@pytest.mark.asyncio
async def test_delete_query_data_calls_delete_object():
    """delete_object вызывается с правильным ключом и бакетом."""
    client = MagicMock()
    client.delete_object = AsyncMock()

    storage = _make_storage()
    with patch.object(storage._session, "client", _make_s3_context(client)):
        await storage.delete_query_data("query_5.html")

    client.delete_object.assert_called_once_with(
        Bucket="test-bucket", Key="query_5.html"
    )


@pytest.mark.asyncio
async def test_delete_query_data_raises_500_on_error():
    """Исключение при удалении приводит к HTTPException 500."""
    client = MagicMock()
    client.delete_object = AsyncMock(side_effect=Exception("connection failed"))

    storage = _make_storage()
    with patch.object(storage._session, "client", _make_s3_context(client)):
        with pytest.raises(HTTPException) as exc_info:
            await storage.delete_query_data("query_5.html")

    assert exc_info.value.status_code == 500
