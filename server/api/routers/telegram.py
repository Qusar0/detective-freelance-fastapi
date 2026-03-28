from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from server.api.database.database import get_db
from server.api.schemas.telegram import (
    WriteSupportRequest,
    WriteSupportResponse,
)
from server.api.dao.telegram_notifications import TelegramNorificationsDAO
from server.bots.support_bot import send_message_async
from server.api.utils.route_handler import handle_route_errors

router = APIRouter(prefix="/telegram", tags=["Telegram"])


@router.get("/connect_tg")
@handle_route_errors("Ошибка при сохранении связи")
async def connect_tg(
    chat: int = Query(..., description="ID чата Telegram"),
    db: AsyncSession = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    Authorize.jwt_required()
    user_id = int(Authorize.get_jwt_subject())

    success = await TelegramNorificationsDAO.save_user_and_chat(user_id, chat, db)
    if not success:
        raise HTTPException(status_code=422, detail="Пользователь уже привязан")
    return {"status": "success", "message": "Телеграмм аккаунт успешно привязан"}


@router.post("/write_support", response_model=WriteSupportResponse)
@handle_route_errors("Ошибка при отправке сообщения")
async def write_support(payload: WriteSupportRequest, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    await send_message_async(payload.theme, payload.description, payload.contacts)
    return {"status": "message sent."}
