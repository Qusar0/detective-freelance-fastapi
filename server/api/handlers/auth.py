from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi_jwt_auth import AuthJWT
from passlib.hash import bcrypt
from starlette.responses import JSONResponse
from server.api.database.database import get_db
from server.api.models.models import Users, UserRole
from server.api.schemas.users import (
    RegisterRequest,
    LoginRequest,
    AuthResponse,
    StatusMessage,
    ResetPasswordRequest
)
from server.api.conf.mail import (
    send_email,
    generate_conformation_token,
    confirm_token,
)
from server.api.templates.email_message import (
    get_confirmation_email,
    get_already_registered_email,
    get_reset_password_email,
)
import logging
from server.api.conf.config import settings


router = APIRouter(prefix="/v1/auth", tags=['auth'])


@router.get("/confirm/{token}", response_model=StatusMessage)
async def confirm_email(token: str, db: AsyncSession = Depends(get_db)):
    try:
        email = confirm_token(token)
        if not email:
            raise HTTPException(
                status_code=400,
                detail="Invalid or expired token",
            )

        result = await db.execute(
            select(Users)
            .where(Users.email == email),
        )
        user = result.scalars().first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.is_confirmed:
            return {"status": "success", "message": "Email already confirmed"}

        user.is_confirmed = True
        await db.commit()

        return {"status": "success", "message": "Email confirmed successfully"}

    except Exception as e:
        logging.error(f"Error confirming email: {str(e)}")
        raise HTTPException(status_code=422, detail="Invalid input")


@router.post("/register", response_model=StatusMessage)
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Users).where(Users.email == data.email)
    )
    existing_user = result.scalars().first()

    if existing_user:
        email_content = get_already_registered_email(
            data.email,
            login_url=f"{settings.frontend_url}/login",
        )
        await send_email(**email_content)
        return {
            "status": "success",
            "message": "На ваш email отправлена информация о существующем аккаунте.",
        }

    role = await db.scalar(
        select(UserRole)
        .where(UserRole.role_name == 'user'),
    )
    hashed_password = bcrypt.hash(data.password)
    user = Users(
        email=data.email,
        password=hashed_password,
        user_role_id=role.id,
    )

    db.add(user)
    await db.commit()

    token = generate_conformation_token(data.email)

    confirm_url = f'{settings.frontend_url}/confirm-email?token={token}'
    email_content = get_confirmation_email(data.email, confirm_url)
    await send_email(**email_content)

    return {
        "status": "success",
        "message": "На ваш email отправлена ссылка для подтверждения.",
    }


@router.post("/login", response_model=AuthResponse)
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    result = await db.execute(select(Users).where(Users.email == data.email))
    user = result.scalars().first()

    if not user or not bcrypt.verify(data.password, user.password):
        raise HTTPException(status_code=422, detail="Неверные данные")

    expires = 604800 if data.stay_logged_in else 21600
    access_token = Authorize.create_access_token(
        subject=str(user.id),
        expires_time=expires,
    )

    response = JSONResponse(
        content={
            "message": "login successful",
            "user_id": user.id,
            "email": user.email,
            "created": str(user.created)
        }
    )

    Authorize.set_access_cookies(access_token, response, max_age=expires)

    return response


@router.post("/logout", response_model=StatusMessage)
async def logout(Authorize: AuthJWT = Depends()):
    response = JSONResponse({"message": "logout successful"})
    Authorize.unset_jwt_cookies(response)
    return response


@router.post("/forgot_password", response_model=StatusMessage)
async def forgot_password(email: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Users).where(Users.email == email))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    token = generate_conformation_token(email)

    reset_url = f"{settings.frontend_url}/reset-password?token={token}"
    email_content = get_reset_password_email(email, reset_url)
    await send_email(**email_content)

    return {
        "status": "success",
        "message": "Ссылка для сброса пароля отправлена на ваш email",
    }


@router.post("/reset_password", response_model=StatusMessage)
async def reset_password(
    data: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        email = confirm_token(data.token)
        if not email:
            raise HTTPException(status_code=400, detail="Недействительный или просроченный токен")

        result = await db.execute(select(Users).where(Users.email == email))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")

        user.password = bcrypt.hash(data.new_password)
        await db.commit()

        return {"status": "success", "message": "Пароль успешно изменён"}

    except Exception as e:
        logging.error(f"Ошибка при сбросе пароля: {str(e)}")
        raise HTTPException(status_code=422, detail="Неверный ввод")