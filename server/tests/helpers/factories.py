from datetime import datetime
from unittest.mock import MagicMock

from passlib.hash import bcrypt


def make_user(
    id: int = 1,
    email: str = "test@example.com",
    is_confirmed: bool = True,
    password_plain: str = "password123",
) -> MagicMock:
    user = MagicMock()
    user.id = id
    user.email = email
    user.is_confirmed = is_confirmed
    user.password = bcrypt.hash(password_plain)
    user.created = datetime(2025, 1, 1, 12, 0, 0)
    user.user_role_id = 1
    return user


def make_user_balance(user_id: int = 1, balance: float = 100.0) -> MagicMock:
    ub = MagicMock()
    ub.id = 1
    ub.user_id = user_id
    ub.balance = balance
    return ub


def make_user_query(
    query_id: int = 1,
    user_id: int = 1,
    status: str = "pending",
    category: str = "name",
    title: str = "Test Query",
) -> MagicMock:
    uq = MagicMock()
    uq.query_id = query_id
    uq.user_id = user_id
    uq.query_status = status
    uq.query_category = category
    uq.query_title = title
    uq.query_created_at = datetime(2025, 1, 1, 12, 0, 0)
    uq.deleted_at = None
    uq.queries_balances = MagicMock(balance=10.0)
    return uq


def make_event(
    event_id: int = 1,
    query_id: int = 1,
    event_type: str = "search_started",
    event_status: str = "new",
) -> MagicMock:
    ev = MagicMock()
    ev.event_id = event_id
    ev.query_id = query_id
    ev.event_type = event_type
    ev.event_status = event_status
    ev.created_time = datetime(2025, 1, 1, 12, 0, 0)
    ev.additional_data = {}
    return ev
