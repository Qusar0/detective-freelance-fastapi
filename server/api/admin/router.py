from fastapi import APIRouter, FastAPI
from server.api.admin.config import init_admin
from server.api.admin.views import (
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
    admin = init_admin(app)
    
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