from fastapi import APIRouter, FastAPI
from server.api.admin.config import init_admin
from server.api.admin.views import (
    UserAdmin,
    UserQueriesAdmin,
    UserBalancesAdmin,
    PaymentHistoryAdmin,
    ServicesBalanceAdmin,
    EventsAdmin
)


router = APIRouter(prefix="/admin", tags=["admin"])


def setup_admin(app: FastAPI):
    admin = init_admin(app)
    
    admin.add_view(UserAdmin)
    admin.add_view(UserQueriesAdmin)
    admin.add_view(UserBalancesAdmin)
    admin.add_view(PaymentHistoryAdmin)
    admin.add_view(ServicesBalanceAdmin)
    admin.add_view(EventsAdmin)
    
    router.mount("/admin", admin) 