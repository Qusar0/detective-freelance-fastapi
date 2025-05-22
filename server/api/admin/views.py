from sqladmin import ModelView
from server.api.models.models import (
    BalanceHistory, Blacklist, Events, Keywords, PaymentHistory,
    ProhibitedSites, QueriesBalance, ServicesBalance, TelegramNotifications,
    TextData, UserBalances, UserQueries, UserRole, Users, Language
)
from typing import Any
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from server.api.database.database import async_session
from fastapi_jwt_auth import AuthJWT
from contextlib import asynccontextmanager


@asynccontextmanager
async def get_session():
    async with async_session() as session:
        yield session


class BalanceHistoryAdmin(ModelView, model=BalanceHistory):
    name = "История баланса"
    name_plural = "История балансов"
    icon = "fa-solid fa-coins"
    
    column_list = [
        BalanceHistory.id,
        BalanceHistory.transaction_type,
        BalanceHistory.amount,
        BalanceHistory.timestamp,
        BalanceHistory.query
    ]
    column_labels = {
        BalanceHistory.id: "ID",
        BalanceHistory.transaction_type: "Тип транзакции",
        BalanceHistory.amount: "Сумма",
        BalanceHistory.timestamp: "Время",
        BalanceHistory.query: "Запрос"
    }
    column_details_list = [
        BalanceHistory.id,
        BalanceHistory.transaction_type,
        BalanceHistory.amount,
        BalanceHistory.timestamp,
        BalanceHistory.query
    ]
    column_searchable_list = [BalanceHistory.transaction_type]
    column_sortable_list = [BalanceHistory.id, BalanceHistory.timestamp, BalanceHistory.amount]
    can_create = False
    can_edit = False
    can_delete = False

class EventsAdmin(ModelView, model=Events):
    name = "Событие"
    name_plural = "События"
    icon = "fa-solid fa-calendar-check"
    
    column_list = [
        Events.event_id,
        Events.event_type,
        Events.event_status,
        Events.query,
        Events.created_time
    ]
    column_labels = {
        Events.event_id: "ID события",
        Events.event_type: "Тип события",
        Events.event_status: "Статус",
        Events.query: "Запрос",
        Events.created_time: "Время создания"
    }
    column_details_exclude_list = [Events.query_id, Events.additional_data]
    column_searchable_list = [Events.event_type, Events.event_status]
    column_sortable_list = [Events.event_id, Events.created_time]
    can_create = False
    can_edit = False

class KeywordsAdmin(ModelView, model=Keywords):
    name = "Ключевое слово"
    name_plural = "Ключевые слова"
    icon = "fa-solid fa-key"
    
    column_list = [Keywords.id, Keywords.word, Keywords.word_type]
    column_labels = {
        Keywords.id: "ID",
        Keywords.word: "Слово",
        Keywords.word_type: "Тип слова"
    }
    column_searchable_list = [Keywords.word, Keywords.word_type]
    column_sortable_list = [Keywords.id, Keywords.word]


class PaymentHistoryAdmin(ModelView, model=PaymentHistory):
    name = "История платежей"
    name_plural = "История платежей"
    icon = "fa-solid fa-credit-card"
    
    column_list = [
        PaymentHistory.id,
        PaymentHistory.user,
        PaymentHistory.payment_amount,
        PaymentHistory.currency,
        PaymentHistory.operation_type,
        PaymentHistory.status,
        PaymentHistory.date_time
    ]
    column_labels = {
        PaymentHistory.id: "ID",
        PaymentHistory.user: "Пользователь",
        PaymentHistory.payment_amount: "Сумма",
        PaymentHistory.currency: "Валюта",
        PaymentHistory.operation_type: "Тип операции",
        PaymentHistory.status: "Статус",
        PaymentHistory.date_time: "Дата и время",
        PaymentHistory.transaction_id: "Номер транзакции",
        PaymentHistory.invoice_id: "Номер инвойс",
        PaymentHistory.email: "Email",
        PaymentHistory.ip_address: "IP адресс",
    }
    column_details_exclude_list = [PaymentHistory.user_id]
    column_searchable_list = [PaymentHistory.status, PaymentHistory.operation_type]
    column_sortable_list = [PaymentHistory.id, PaymentHistory.date_time, PaymentHistory.payment_amount]
    can_create = False
    can_edit = False


class ProhibitedSitesAdmin(ModelView, model=ProhibitedSites):
    name = "Запрещенный сайт"
    name_plural = "Запрещенные сайты"
    icon = "fa-solid fa-globe"
    
    column_list = [ProhibitedSites.id, ProhibitedSites.site_link]
    column_labels = {
        ProhibitedSites.id: "ID",
        ProhibitedSites.site_link: "Ссылка на сайт"
    }
    column_searchable_list = [ProhibitedSites.site_link]
    column_sortable_list = [ProhibitedSites.id]


class QueriesBalanceAdmin(ModelView, model=QueriesBalance):
    name = "Баланс запроса"
    name_plural = "Балансы запросов"
    icon = "fa-solid fa-file-invoice-dollar"
    
    column_list = [
        QueriesBalance.id,
        QueriesBalance.query,
        QueriesBalance.balance,
        QueriesBalance.transaction_date
    ]
    column_labels = {
        QueriesBalance.id: "ID",
        QueriesBalance.query: "Запрос",
        QueriesBalance.balance: "Баланс",
        QueriesBalance.transaction_date: "Дата транзакции"
    }
    column_details_exclude_list = [QueriesBalance.query_id]
    column_searchable_list = []
    column_sortable_list = [QueriesBalance.id, QueriesBalance.transaction_date]
    can_create = False
    can_delete = False

class ServicesBalanceAdmin(ModelView, model=ServicesBalance):
    name = "Баланс сервиса"
    name_plural = "Балансы сервисов"
    icon = "fa-solid fa-server"
    
    column_list = [
        ServicesBalance.id,
        ServicesBalance.service_name,
        ServicesBalance.balance
    ]
    column_labels = {
        ServicesBalance.id: "ID",
        ServicesBalance.service_name: "Название сервиса",
        ServicesBalance.balance: "Баланс"
    }
    column_searchable_list = [ServicesBalance.service_name]
    column_sortable_list = [ServicesBalance.id, ServicesBalance.balance]


class TelegramNotificationsAdmin(ModelView, model=TelegramNotifications):
    name = "Телеграм уведомления"
    name_plural = "Телеграм уведомления"
    icon = "fa-solid fa-user"
    
    column_list = [
        TelegramNotifications.id,
        TelegramNotifications.user,
        TelegramNotifications.chat_id
    ]
    column_labels = {
        TelegramNotifications.id: "ID",
        TelegramNotifications.user: "Пользователь",
        TelegramNotifications.chat_id: "ID чата"
    }
    column_details_exclude_list = [TelegramNotifications.user_id]
    column_searchable_list = [TelegramNotifications.chat_id]
    column_sortable_list = [TelegramNotifications.id]


class TextDataAdmin(ModelView, model=TextData):
    name = "Текстовые данные"
    name_plural = "Текстовые данные"
    icon = "fa-solid fa-file-lines"
    
    column_list = [
        TextData.id,
        TextData.query,
        TextData.file_path
    ]
    column_labels = {
        TextData.id: "ID",
        TextData.query: "Запрос",
        TextData.file_path: "Путь к файлу"
    }
    column_details_exclude_list = [TextData.query_id]
    column_searchable_list = [TextData.file_path]
    column_sortable_list = [TextData.id]
    can_delete = False
    can_edit = False
    can_create = False

class UserBalancesAdmin(ModelView, model=UserBalances):
    name = "Баланс пользователя"
    name_plural = "Балансы пользователей"
    icon = "fa-solid fa-wallet"
    
    column_list = [
        UserBalances.id,
        UserBalances.user,
        UserBalances.balance
    ]
    column_labels = {
        UserBalances.id: "ID",
        UserBalances.user: "Пользователь",
        UserBalances.balance: "Баланс"
    }
    column_details_exclude_list = [UserBalances.user_id]
    column_searchable_list = []
    column_sortable_list = [UserBalances.id, UserBalances.balance]
    can_delete = False
    can_create = False

class UserQueriesAdmin(ModelView, model=UserQueries):
    name = "Запрос пользователя"
    name_plural = "Запросы пользователей"
    icon = "fa-solid fa-magnifying-glass"
    
    column_list = [
        UserQueries.query_id,
        UserQueries.user,
        UserQueries.query_status,
        UserQueries.query_category,
        UserQueries.query_created_at,
        UserQueries.query_title
    ]
    column_labels = {
        UserQueries.query_id: "ID запроса",
        UserQueries.user: "Пользователь",
        UserQueries.query_status: "Статус",
        UserQueries.query_category: "Категория",
        UserQueries.query_created_at: "Дата создания",
        UserQueries.query_title: "Название",
        UserQueries.balance_histories: "История баланса",
        UserQueries.text_dates: "Расположение запроса",
        UserQueries.queries_balances: "Стоимость запроса",
        UserQueries.events: "Уведомление"
    }
    column_details_exclude_list = [
        UserQueries.user_id,
        UserQueries.query_unix_date,
        UserQueries.deleted_at,
    ]
    column_searchable_list = [
        UserQueries.query_status,
        UserQueries.query_category,
        UserQueries.query_title
    ]
    column_sortable_list = [
        UserQueries.query_id,
        UserQueries.query_created_at
    ]


class UserRoleAdmin(ModelView, model=UserRole):
    name = "Роль пользователя"
    name_plural = "Роли пользователей"
    icon = "fa-solid fa-user-tag"
    
    column_list = [
        UserRole.id,
        UserRole.role_name,
        UserRole.users
    ]
    column_labels = {
        UserRole.id: "ID",
        UserRole.role_name: "Название роли",
        UserRole.users: "Пользователи"
    }
    column_searchable_list = [UserRole.role_name]
    column_sortable_list = [UserRole.id]
    form_columns = [UserRole.role_name]


class UsersAdmin(ModelView, model=Users):
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"
    
    column_list = [
        Users.id,
        Users.email,
        Users.is_confirmed,
        Users.user_role,
        Users.created,
        Users.last_visited,
    ]
    column_labels = {
        Users.id: "ID",
        Users.email: "Email",
        Users.is_confirmed: "Подтвержден",
        Users.user_role: "Роль",
        Users.created: "Дата создания",
        Users.user_balance: "Баланс",
        Users.user_queries: "Запросы",
        Users.payment_histories: "Пополнения",
        Users.telegram_notification: "Телеграм",
        Users.confirmation_date: "Дата подтверждения",
        Users.last_visited: "Последнее посещение",
    }
    column_details_exclude_list = [Users.user_role_id, Users.password]
    column_searchable_list = [Users.email]
    column_sortable_list = [Users.id, Users.created]

    can_create = False
    can_edit = False