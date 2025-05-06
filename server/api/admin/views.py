from datetime import datetime, timedelta
from sqladmin import ModelView
from sqladmin.forms import ModelConverter
from server.api.models.models import (
    Users, UserQueries, UserBalances, PaymentHistory,
    ServicesBalance, UserRole, Events, BalanceHistory
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from server.api.database.database import async_session
from fastapi_jwt_auth import AuthJWT
from typing import Any, Optional
from contextlib import asynccontextmanager

@asynccontextmanager
async def get_session():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

async def get_role_id_by_name(role_name: str, session: AsyncSession) -> int | None:
    result = await session.execute(
        select(UserRole).where(UserRole.role_name == role_name)
    )
    role = result.scalar_one_or_none()
    return role.id if role else None

async def is_admin(user_id: int, session: AsyncSession) -> bool:
    admin_role_id = await get_role_id_by_name("admin", session)
    if not admin_role_id:
        return False
    
    result = await session.execute(
        select(Users).where(
            Users.id == user_id,
            Users.user_role_id == admin_role_id
        )
    )
    user = result.scalar_one_or_none()
    return user is not None

async def get_user_roles_choices(session: AsyncSession) -> list[tuple[int, str]]:
    result = await session.execute(select(UserRole))
    roles = result.scalars().all()
    return [(role.id, role.role_name) for role in roles]

class UserAdmin(ModelView, model=Users):
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"
    column_list = [Users.id, Users.email, Users.is_confirmed, Users.created, Users.user_role_id]
    column_labels = {
        Users.id: "ID",
        Users.email: "Email",
        Users.is_confirmed: "Подтвержден",
        Users.created: "Дата создания",
        Users.user_role_id: "Роль"
    }
    column_searchable_list = [Users.email]
    column_sortable_list = [Users.id, Users.email, Users.created]
    column_details_exclude_list = [Users.password]
    form_columns = [Users.email, Users.is_confirmed, Users.user_role_id]
    form_labels = {
        Users.email: "Email",
        Users.is_confirmed: "Подтвержден",
        Users.user_role_id: "Роль"
    }
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    async def is_accessible(self, request) -> bool:
        try:
            auth = AuthJWT(request)
            auth.jwt_required()
            user_id = int(auth.get_jwt_subject())
            
            async with get_session() as session:
                return await is_admin(user_id, session)
        except Exception:
            return False

    async def get_form_choices(self, request, field_name: str) -> list[tuple]:
        if field_name == "user_role_id":
            async with get_session() as session:
                return await get_user_roles_choices(session)
        return []

class UserQueriesAdmin(ModelView, model=UserQueries):
    name = "Запрос"
    name_plural = "Запросы"
    icon = "fa-solid fa-magnifying-glass"
    column_list = [
        UserQueries.query_id,
        UserQueries.user_id,
        UserQueries.query_status,
        UserQueries.query_category,
        UserQueries.query_created_at,
        UserQueries.query_title
    ]
    column_labels = {
        UserQueries.query_id: "ID запроса",
        UserQueries.user_id: "ID пользователя",
        UserQueries.query_status: "Статус",
        UserQueries.query_category: "Категория",
        UserQueries.query_created_at: "Дата создания",
        UserQueries.query_title: "Название"
    }
    column_searchable_list = [UserQueries.query_id, UserQueries.user_id, UserQueries.query_title]
    column_sortable_list = [UserQueries.query_id, UserQueries.user_id, UserQueries.query_created_at]
    form_columns = [
        UserQueries.user_id,
        UserQueries.query_status,
        UserQueries.query_category,
        UserQueries.query_title
    ]
    form_labels = {
        UserQueries.user_id: "ID пользователя",
        UserQueries.query_status: "Статус",
        UserQueries.query_category: "Категория",
        UserQueries.query_title: "Название"
    }
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    async def is_accessible(self, request) -> bool:
        try:
            auth = AuthJWT(request)
            auth.jwt_required()
            user_id = int(auth.get_jwt_subject())
            
            async with get_session() as session:
                return await is_admin(user_id, session)
        except Exception:
            return False

    async def get_list_query(self, request) -> Any:
        query = await super().get_list_query(request)
        
        # Фильтр по категории
        category = request.query_params.get("category")
        if category:
            query = query.where(UserQueries.query_category == category)
            
        # Фильтр по статусу
        status = request.query_params.get("status")
        if status:
            query = query.where(UserQueries.query_status == status)
            
        # Фильтр по дате
        date_range = request.query_params.get("date_range")
        if date_range:
            now = datetime.utcnow()
            if date_range == "last_day":
                start_date = now - timedelta(days=1)
            elif date_range == "last_week":
                start_date = now - timedelta(weeks=1)
            elif date_range == "last_month":
                start_date = now - timedelta(days=30)
            else:
                start_date = None
                
            if start_date:
                query = query.where(UserQueries.query_created_at >= start_date)
                
        return query

class UserBalancesAdmin(ModelView, model=UserBalances):
    name = "Баланс пользователя"
    name_plural = "Балансы пользователей"
    icon = "fa-solid fa-wallet"
    column_list = [UserBalances.id, UserBalances.user_id, UserBalances.balance]
    column_labels = {
        UserBalances.id: "ID",
        UserBalances.user_id: "ID пользователя",
        UserBalances.balance: "Баланс"
    }
    column_searchable_list = [UserBalances.user_id]
    column_sortable_list = [UserBalances.id, UserBalances.balance]
    form_columns = [UserBalances.user_id, UserBalances.balance]
    form_labels = {
        UserBalances.user_id: "ID пользователя",
        UserBalances.balance: "Баланс"
    }
    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True

    async def is_accessible(self, request) -> bool:
        try:
            auth = AuthJWT(request)
            auth.jwt_required()
            user_id = int(auth.get_jwt_subject())
            
            async with get_session() as session:
                return await is_admin(user_id, session)
        except Exception:
            return False

class PaymentHistoryAdmin(ModelView, model=PaymentHistory):
    name = "История платежей"
    name_plural = "История платежей"
    icon = "fa-solid fa-credit-card"
    column_list = [
        PaymentHistory.id,
        PaymentHistory.user_id,
        PaymentHistory.payment_amount,
        PaymentHistory.currency,
        PaymentHistory.operation_type,
        PaymentHistory.status,
        PaymentHistory.date_time
    ]
    column_labels = {
        PaymentHistory.id: "ID",
        PaymentHistory.user_id: "ID пользователя",
        PaymentHistory.payment_amount: "Сумма",
        PaymentHistory.currency: "Валюта",
        PaymentHistory.operation_type: "Тип операции",
        PaymentHistory.status: "Статус",
        PaymentHistory.date_time: "Дата и время"
    }
    column_searchable_list = [PaymentHistory.user_id, PaymentHistory.status, PaymentHistory.operation_type]
    column_sortable_list = [PaymentHistory.id, PaymentHistory.payment_amount, PaymentHistory.date_time]
    form_columns = [
        PaymentHistory.user_id,
        PaymentHistory.payment_amount,
        PaymentHistory.currency,
        PaymentHistory.operation_type,
        PaymentHistory.status
    ]
    form_labels = {
        PaymentHistory.user_id: "ID пользователя",
        PaymentHistory.payment_amount: "Сумма",
        PaymentHistory.currency: "Валюта",
        PaymentHistory.operation_type: "Тип операции",
        PaymentHistory.status: "Статус"
    }
    can_create = True
    can_edit = False
    can_delete = False
    can_view_details = True

    async def is_accessible(self, request) -> bool:
        try:
            auth = AuthJWT(request)
            auth.jwt_required()
            user_id = int(auth.get_jwt_subject())
            
            async with get_session() as session:
                return await is_admin(user_id, session)
        except Exception:
            return False

class ServicesBalanceAdmin(ModelView, model=ServicesBalance):
    name = "Баланс сервисов"
    name_plural = "Балансы сервисов"
    icon = "fa-solid fa-server"
    column_list = [ServicesBalance.id, ServicesBalance.service_name, ServicesBalance.balance]
    column_labels = {
        ServicesBalance.id: "ID",
        ServicesBalance.service_name: "Название сервиса",
        ServicesBalance.balance: "Баланс"
    }
    column_searchable_list = [ServicesBalance.service_name]
    column_sortable_list = [ServicesBalance.id, ServicesBalance.balance]
    form_columns = [ServicesBalance.service_name, ServicesBalance.balance]
    form_labels = {
        ServicesBalance.service_name: "Название сервиса",
        ServicesBalance.balance: "Баланс"
    }
    can_create = True
    can_edit = False
    can_delete = False
    can_view_details = True

    async def is_accessible(self, request) -> bool:
        try:
            auth = AuthJWT(request)
            auth.jwt_required()
            user_id = int(auth.get_jwt_subject())
            
            async with get_session() as session:
                return await is_admin(user_id, session)
        except Exception:
            return False

class EventsAdmin(ModelView, model=Events):
    name = "Событие"
    name_plural = "События"
    icon = "fa-solid fa-calendar"
    column_list = [
        Events.event_id,
        Events.event_type,
        Events.event_status,
        Events.query_id,
        Events.created_time
    ]
    column_labels = {
        Events.event_id: "ID события",
        Events.event_type: "Тип события",
        Events.event_status: "Статус",
        Events.query_id: "ID запроса",
        Events.created_time: "Время создания"
    }
    column_searchable_list = [Events.event_type, Events.event_status]
    column_sortable_list = [Events.event_id, Events.created_time]
    form_columns = [
        Events.event_type,
        Events.event_status,
        Events.query_id,
        Events.additional_data
    ]
    form_labels = {
        Events.event_type: "Тип события",
        Events.event_status: "Статус",
        Events.query_id: "ID запроса",
        Events.additional_data: "Дополнительные данные"
    }
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True

    async def is_accessible(self, request) -> bool:
        try:
            auth = AuthJWT(request)
            auth.jwt_required()
            user_id = int(auth.get_jwt_subject())
            
            async with get_session() as session:
                return await is_admin(user_id, session)
        except Exception:
            return False
