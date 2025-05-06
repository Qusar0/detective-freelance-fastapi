from typing import Optional
from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from fastapi import Request, Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.future import select
from server.api.models.models import (
    Users, UserQueries, UserBalances, PaymentHistory,
    ServicesBalance, UserRole, Events, BalanceHistory
)
from server.api.database.database import get_db, engine
from server.api.conf.config import settings

class AdminAuth(AuthenticationBackend):
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.middlewares = []

    async def login(self, request: Request) -> bool:
        return True

    async def logout(self, request: Request) -> bool:
        return True

    async def authenticate(self, request: Request) -> bool:
        try:
            auth = AuthJWT(request)
            auth.jwt_required()
            user_id = int(auth.get_jwt_subject())

            db = await anext(get_db())
            result = await db.execute(
                select(Users)
                .join(UserRole)
                .where(
                    Users.id == user_id,
                    UserRole.role_name == "admin"
                )
            )
            user = result.scalar_one_or_none()
            
            return user is not None
        except Exception:
            return False

def init_admin(app: FastAPI) -> Admin:
    admin = Admin(
        app=app,
        engine=engine,
        authentication_backend=AdminAuth(secret_key=settings.secret_key),
        templates_dir="templates",
        title="Admin Panel",
        logo_url="https://example.com/logo.png",
    )
    return admin 