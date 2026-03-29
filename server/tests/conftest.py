import os
import sys
from unittest.mock import MagicMock

os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5432")
os.environ.setdefault("DB_NAME", "test_db")
os.environ.setdefault("DB_USER", "test_user")
os.environ.setdefault("DB_PASS", "test_pass")
os.environ.setdefault("SECRET_KEY", "test-secret-key-32chars-xxxxxxxxx")
os.environ.setdefault("JWT_SECRET_KEY", "test-jwt-secret-key-32chars-xxxxx")
os.environ.setdefault("MAIL_USERNAME", "test@test.com")
os.environ.setdefault("MAIL_PASSWORD", "testpass")
os.environ.setdefault("MAIL_DEFAULT_SENDER", "test@test.com")
os.environ.setdefault("MAIL_PORT", "587")
os.environ.setdefault("MAIL_SERVER", "smtp.test.com")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("SECURITY_PASSWORD_SALT", "test-salt")
os.environ.setdefault("TELEGRAM_API_ID", "12345")
os.environ.setdefault("TELEGRAM_API_HASH", "testhash")
os.environ.setdefault("TELEGRAM_BOT_TOKEN", "123:testtoken")
os.environ.setdefault("TELEGRAM_DB_ENCRYPTION_KEY", "testkey")
os.environ.setdefault("ADMIN_CHAT_ID", "12345")
os.environ.setdefault("BALANCE_THRESHOLD", "100")
os.environ.setdefault("CHECK_INTERVAL", "60")
os.environ.setdefault("NOTIFICATION_BOT_TOKEN", "456:notifytoken")
os.environ.setdefault("SUPPORT_BOT_TOKEN", "789:supporttoken")
os.environ.setdefault("XML_RIVER_USER_ID", "testuser")
os.environ.setdefault("XML_RIVER_API_KEY", "testapikey")
os.environ.setdefault("UTILS_TOKEN", "testutils")
os.environ.setdefault("LIGHTHOUSE_URL", "http://localhost:3000")
os.environ.setdefault("FRONTEND_URL", "http://localhost:5173")
os.environ.setdefault("IRBIS_TOKEN", "testirbis")
os.environ.setdefault("MORPHER_TOKEN", "testmorpher")

_mock_redis = MagicMock()
_mock_redis.StrictRedis.from_url.return_value = MagicMock()
_mock_redis_asyncio = MagicMock()
_mock_redis_asyncio.from_url.return_value = MagicMock()
_mock_redis.asyncio = _mock_redis_asyncio
sys.modules["redis"] = _mock_redis
sys.modules["redis.asyncio"] = _mock_redis_asyncio

_mock_aiogram = MagicMock()
_mock_aiogram.Bot.return_value = MagicMock()
sys.modules["aiogram"] = _mock_aiogram
sys.modules["aiogram.types"] = MagicMock()
sys.modules["aiogram.contrib"] = MagicMock()
sys.modules["aiogram.contrib.fsm_storage"] = MagicMock()
sys.modules["aiogram.contrib.fsm_storage.memory"] = MagicMock()

sys.modules["celery"] = MagicMock()

import pytest  # noqa: E402
