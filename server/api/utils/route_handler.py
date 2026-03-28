from functools import wraps
from loguru import logger
from fastapi import HTTPException
from fastapi_jwt_auth.exceptions import MissingTokenError
from server.api.dao.user_balances import InsufficientFundsError


def handle_route_errors(error_msg: str = "Внутренняя ошибка сервера"):
    """
    Декоратор для обработки ошибок в FastAPI-эндпоинтах.

    Обрабатывает:
    - HTTPException
    - MissingTokenError - 401 Unauthorized
    - InsufficientFundsError - 400 Bad Request
    - Exception - 500
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except HTTPException:
                raise
            except MissingTokenError:
                logger.error("Неавторизованный пользователь")
                raise HTTPException(status_code=401, detail="Неавторизованный пользователь")
            except InsufficientFundsError:
                raise HTTPException(status_code=400, detail="Недостаточно средств")
            except Exception as e:
                logger.opt(exception=True).error(f"{error_msg}: {e}")
                raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")
        return wrapper
    return decorator
