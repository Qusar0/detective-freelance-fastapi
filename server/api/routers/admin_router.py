from fastapi import APIRouter
from fastapi import FastAPI
from sqladmin import Admin

from server.api.conf.config import settings
from server.api.database.database import engine
from server.api.routers.admin.admin_auth import AdminAuth
from server.api.routers.admin.views import (
    BalanceHistoryAdmin,
    EventsAdmin,
    KeywordsAdmin,
    PaymentHistoryAdmin,
    ProhibitedSitesAdmin,
    ProhibitedPhoneSitesAdmin,
    QueriesBalanceAdmin,
    ServicesBalanceAdmin,
    TelegramNotificationsAdmin,
    TextDataAdmin,
    UserBalancesAdmin,
    UserQueriesAdmin,
    UserRoleAdmin,
    UsersAdmin,
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

    admin.add_view(BalanceHistoryAdmin)
    admin.add_view(EventsAdmin)
    admin.add_view(KeywordsAdmin)
    admin.add_view(PaymentHistoryAdmin)
    admin.add_view(ProhibitedSitesAdmin)
    admin.add_view(ProhibitedPhoneSitesAdmin)
    admin.add_view(QueriesBalanceAdmin)
    admin.add_view(ServicesBalanceAdmin)
    admin.add_view(TelegramNotificationsAdmin)
    admin.add_view(TextDataAdmin)
    admin.add_view(UserBalancesAdmin)
    admin.add_view(UserQueriesAdmin)
    admin.add_view(UserRoleAdmin)
    admin.add_view(UsersAdmin)

    router.mount("/admin", admin)
