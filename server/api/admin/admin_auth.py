from contextlib import asynccontextmanager

from fastapi import Request
from fastapi_jwt_auth import AuthJWT
from passlib.hash import bcrypt
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy.future import select
from starlette.responses import RedirectResponse

from server.api.conf.config import settings
from server.api.database.database import async_session
from server.api.models.models import UserRole, Users


@asynccontextmanager
async def get_session():
    async with async_session() as session:
        yield session


class AdminAuth(AuthenticationBackend):
    def __init__(self, secret_key: str):
        super().__init__(secret_key)

    async def login(self, request: Request) -> bool:
        form = await request.form()
        email = form.get("username")
        password = form.get("password")

        if not email or not password:
            return False

        try:
            async with get_session() as db:
                result = await db.execute(
                    select(Users)
                    .join(UserRole)
                    .where(
                        Users.email == email,
                        UserRole.role_name.in_(["admin"])
                    )
                )
                user = result.scalar_one_or_none()

                if not user:
                    return False

                if not bcrypt.verify(password, user.password):
                    return False

                auth = AuthJWT(request)
                response = RedirectResponse(url="/admin")
                access_token = auth.create_access_token(
                    subject=str(user.id),
                    expires_time=86400
                )
                request.session.update({"access_token": access_token})
                request.state.response = response
                return True
        except Exception as e:
            print(f"Admin login error: {e}")
            return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()

        temp_response = RedirectResponse(url="/admin/login")
        auth = AuthJWT(req=request, res=temp_response)
        auth.unset_jwt_cookies(temp_response)

        request.state.response = temp_response
        return True

    async def authenticate(self, request: Request) -> RedirectResponse | bool:
        access_token = request.session.get("access_token")
        if not access_token:
            return RedirectResponse(url="/admin/login")

        try:
            response = RedirectResponse(url="/admin")
            auth = AuthJWT(req=request, res=response)
            auth._token = access_token
            auth.set_access_cookies(access_token, response, max_age=settings.access_token_expire_minutes)
            user_id = int(auth.get_jwt_subject())

            async with async_session() as session:
                result = await session.execute(
                    select(Users)
                    .join(UserRole)
                    .where(
                        Users.id == user_id,
                        UserRole.role_name.in_(["admin"])
                    )
                )
                user = result.scalar_one_or_none()
                if not user:
                    return RedirectResponse(url="/admin/login")

            return True

        except Exception as e:
            print(f"Admin auth error: {e}")
            return RedirectResponse(url="/admin/login")
