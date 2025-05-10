from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from fastapi_jwt_auth import AuthJWT
import logging
from server.bots.support_bot import send_message_async
from server.api.scripts import utils
from server.api.schemas.telegram import (
    WriteSupportRequest,
    WriteSupportResponse,
)
from sqlalchemy.ext.asyncio import AsyncSession
from server.api.database.database import get_db
from server.api.conf.config import settings


router = APIRouter(prefix="/telegram", tags=["Telegram"])


@router.get("/connect_tg", response_class=RedirectResponse)
async def connect_tg(
    chat: int = Query(..., description="ID чата Telegram"),
    db: AsyncSession = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    try:
        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())
    except Exception as why:
        logging.warning("Invalid token: " + str(why))
        raise HTTPException(status_code=422, detail="Invalid token")

    try:
        success = await utils.save_user_and_chat(user_id, chat, db)
        if not success:
            raise HTTPException(status_code=422, detail="Пользователь уже привязан")
    except HTTPException:
        raise
    except Exception as e:
        logging.warning("Ошибка при сохранении связи: " + str(e))
        raise HTTPException(status_code=422, detail="Неверные данные")

    return RedirectResponse(url=settings.frontend_url)


@router.post("/write_support", response_model=WriteSupportResponse)
async def write_support(payload: WriteSupportRequest, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as why:
        logging.warning("Invalid token: " + str(why))
        raise HTTPException(status_code=422, detail="Invalid token")

    try:
        await send_message_async(payload.theme, payload.description, payload.contacts)
    except Exception as e:
        logging.warning("Ошибка при отправке сообщения: " + str(e))
        raise HTTPException(status_code=422, detail="Ошибка отправки")

    return {"status": "message sent."}
