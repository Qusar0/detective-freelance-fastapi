from fastapi import APIRouter
from fastapi import FastAPI
from sqladmin import Admin

from server.api.conf.config import settings
from server.api.database.database import engine
from server.api.admin.admin_auth import AdminAuth
from server.api.admin.views import (
    balance_history_admin,
    events_admin,
    keywords_admin,
    payment_history_admin,
    prohibited_phone_sites_admin,
    prohibited_sites_admin,
    queries_balance_admin,
    services_balance_admin,
    telegram_notifications_admin,
    text_data_admin,
    user_balances_admin,
    user_queries_admin,
    user_role_admin,
    users_admin,
)


router = APIRouter(prefix="/admin", tags=["admin"])


def setup_admin(app: FastAPI):
    admin = Admin(
        app=app,
        engine=engine,
        templates_dir="templates",
        title="Панель администратора",
        authentication_backend=AdminAuth(secret_key=settings.secret_key),
    )

    admin.add_view(balance_history_admin.BalanceHistoryAdmin)
    admin.add_view(events_admin.EventsAdmin)
    admin.add_view(keywords_admin.KeywordsAdmin)
    admin.add_view(payment_history_admin.PaymentHistoryAdmin)
    admin.add_view(prohibited_sites_admin.ProhibitedSitesAdmin)
    admin.add_view(prohibited_phone_sites_admin.ProhibitedPhoneSitesAdmin)
    admin.add_view(queries_balance_admin.QueriesBalanceAdmin)
    admin.add_view(services_balance_admin.ServicesBalanceAdmin)
    admin.add_view(telegram_notifications_admin.TelegramNotificationsAdmin)
    admin.add_view(text_data_admin.TextDataAdmin)
    admin.add_view(user_balances_admin.UserBalancesAdmin)
    admin.add_view(user_queries_admin.UserQueriesAdmin)
    admin.add_view(user_role_admin.UserRoleAdmin)
    admin.add_view(users_admin.UsersAdmin)

    router.mount("/admin", admin)
