from loguru import logger
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import MissingTokenError

from server.api.database.database import get_db
from server.api.dao.users import UsersDAO
from server.api.scripts.sse_manager import (
    event_generator,
    add_subscriber,
)


router = APIRouter(prefix="/sse", tags=['SSE'])


@router.get("/{channel}")
async def sse_endpoint(
    channel: str,
    request: Request,
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db)
):
    try:
        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())

        await UsersDAO.update_last_visit(user_id, db)

        queue = asyncio.Queue()
        await add_subscriber(channel, queue)
        return StreamingResponse(
            event_generator(channel, queue, request),
            media_type="text/event-stream",
        )
    except MissingTokenError:
        logger.error('Неавторизованный пользователь')
        raise HTTPException(status_code=401, detail="Неавторизованный пользователь")
    except Exception as e:
        logger.error(f"Ошибка обновления последнего посещения: {e}")
        await db.rollback()
