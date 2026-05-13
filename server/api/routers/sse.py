import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Request
from server.api.security import oauth2_scheme
from fastapi.responses import StreamingResponse
from fastapi_jwt_auth import AuthJWT

from server.api.database.database import get_db
from server.api.dao.users import UsersDAO
from server.api.scripts.sse_manager import (
    event_generator,
    add_subscriber,
)
from server.api.utils.route_handler import handle_route_errors


router = APIRouter(
    prefix="/sse",
    tags=["SSE"],
    dependencies=[Depends(oauth2_scheme)],
)


@router.get("/{channel}")
@handle_route_errors("Ошибка обновления последнего посещения")
async def sse_endpoint(
    channel: str,
    request: Request,
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db)
):
    Authorize.jwt_required()
    user_id = int(Authorize.get_jwt_subject())

    await UsersDAO.update_last_visit(user_id, db)

    queue = asyncio.Queue()
    await add_subscriber(channel, queue)
    return StreamingResponse(
        event_generator(channel, queue, request),
        media_type="text/event-stream",
    )
