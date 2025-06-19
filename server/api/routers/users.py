import logging
from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from server.api.database.database import get_db
from server.api.schemas.users import (
    AuthStatusResponse,
    TopUpBalanceResponse,
    TopUpBalanceQueryParams,
    ConfirmResponse,
    ChangeEventStatusRequest,
    ChangePasswordRequest,
)
from typing import Dict
from passlib.hash import bcrypt

from server.api.models.models import UserQueries, Events, PaymentHistory, UserBalances, Users
from server.api.scripts.mail import send_confirmation_email, send_email
from server.api.templates.email_message import get_password_changed_email
from server.api.scripts.sse_manager import publish_event
from server.api.scripts.utils import generate_sse_message_type


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/is_authenticated", response_model=AuthStatusResponse)
def is_authenticated(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return {"status": "success", "message": "User authenticated"}


@router.get("/get_events")
async def get_events(
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    try:
        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())
    except Exception as e:
        logging.warning(f"Invalid token: {e}")
        raise HTTPException(status_code=422, detail="Invalid token")

    result = await db.execute(
        select(Events)
        .join(UserQueries, UserQueries.query_id == Events.query_id)
        .where(UserQueries.user_id == user_id)
        .order_by(Events.created_time.desc())
    )
    event_rows = result.scalars().all()

    events: Dict[int, Dict] = {}
    for idx, row in enumerate(event_rows):
        event_data = dict(row.additional_data)
        event_data.update({
            "event_id": row.event_id,
            "event_type": row.event_type,
            "created_time": str(row.created_time),
            "event_status": row.event_status
        })
        events[idx] = event_data

    return events


@router.post("/change_event_status", status_code=200)
async def change_event_status(
    payload: ChangeEventStatusRequest,
    db: AsyncSession = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    try:
        Authorize.jwt_required()

        event_id = payload.event_id

        result = await db.execute(
            select(Events)
            .where(Events.event_id == event_id),
        )
        event = result.scalar_one_or_none()

        if not event:
            raise HTTPException(
                status_code=404,
                detail="Событие не найдено",
            )

        event.event_status = "seen"
        await db.commit()

        return {"message": "Статус успешно изменен"}

    except HTTPException:
        raise
    except Exception as e:
        logging.error("Ошибка изменения статуса события: " + str(e))
        raise HTTPException(
            status_code=422,
            detail="Неверные данные",
        )


@router.get("/get_balance")
async def get_balance(
    db: AsyncSession = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    try:
        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())
    except Exception as e:
        logging.info("Invalid token: " + str(e))
        raise HTTPException(status_code=422, detail="Invalid token")

    result = await db.execute(
        select(UserBalances)
        .where(UserBalances.user_id == user_id),
    )
    balance_entry = result.scalar_one_or_none()

    if not balance_entry:
        raise HTTPException(status_code=404, detail="Balance not found")

    return round(float(balance_entry.balance), 2)


@router.get("/is_confirmed", response_model=ConfirmResponse)
async def is_user_confirmed_endpoint(
    db: AsyncSession = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    try:
        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())

        result = await db.execute(select(Users).where(Users.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.is_confirmed:
            return ConfirmResponse(status="Confirmed", message="User confirmed")

        await send_confirmation_email(user)

        raise HTTPException(
            status_code=401,
            detail="На ваш email повторно выслано сообщение с подтверждением почты"
        )

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Ошибка проверки подтверждения email: {e}")
        raise HTTPException(
            status_code=400,
            detail="Ошибка при проверке или отправке подтверждения",
        )


@router.post("/top_up_balance", response_model=TopUpBalanceResponse)
async def top_up_balance(
    params: TopUpBalanceQueryParams = Body(...),
    db: AsyncSession = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    try:
        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())
    except Exception as e:
        logging.warning(f"Invalid token: {e}")
        raise HTTPException(status_code=422, detail="Invalid token")

    result = await db.execute(
        select(Users)
        .where(Users.id == user_id),
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    if not user.is_confirmed:
        await send_confirmation_email(user)
        raise HTTPException(
            status_code=403,
            detail={
                "status": "error",
                "message": "Для пополнения баланса необходимо подтвердить email. Ссылка отправлена повторно.",
            }
        )

    try:
        payment = PaymentHistory(
            transaction_id=params.transaction_id,
            currency=params.currency,
            payment_amount=params.payment_amount,
            operation_type=params.operation_type,
            invoice_id=params.invoice_id,
            user_id=params.account_id,
            email=params.email,
            date_time=params.date_time.replace(tzinfo=None),
            ip_address=params.ip_address,
            status=params.status,
        )
        db.add(payment)

        if params.status == "Completed":
            result = await db.execute(
                select(UserBalances)
                .where(UserBalances.user_id == params.account_id),
            )
            user_balance = result.scalar_one_or_none()
            if not user_balance:
                raise HTTPException(
                    status_code=404,
                    detail="User balance not found",
                )

            user_balance.balance += params.payment_amount
            db.add(user_balance)

        await db.commit()

        channel = await generate_sse_message_type(user_id, db)

        await publish_event(channel, {
            "event_type": "balance",
            "balance": user_balance.balance,
        })

        return {
            "status": "success",
            "message": "Баланс успешно пополнен",
            "data": {
                "new_balance": round(float(user_balance.balance), 2),
                "transaction_id": params.transaction_id,
                "amount": params.payment_amount,
                "currency": params.currency,
                "operation_date": params.date_time,
                "invoice_id": params.invoice_id,
            }
        }

    except Exception as e:
        logging.warning(f"Invalid input: {e}")
        raise HTTPException(status_code=422, detail="Invalid input")


@router.post("/change_password")
async def change_password(
    data: ChangePasswordRequest,
    db: AsyncSession = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    try:
        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())
    except Exception as e:
        logging.warning(f"Invalid token: {e}")
        raise HTTPException(status_code=422, detail="Invalid token")

    result = await db.execute(select(Users).where(Users.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    if not bcrypt.verify(data.old_password, user.password):
        raise HTTPException(status_code=403, detail="Неверный текущий пароль")

    user.password = bcrypt.hash(data.new_password)
    db.add(user)
    await db.commit()

    email_content = get_password_changed_email(user.email)
    await send_email(**email_content)

    return {"status": "success", "message": "Пароль успешно изменён"}
