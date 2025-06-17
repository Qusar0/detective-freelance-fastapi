from server.api.routers.admin.views.balance_history_admin import BalanceHistoryAdmin
from server.api.routers.admin.views.events_admin import EventsAdmin
from server.api.routers.admin.views.keywords_admin import KeywordsAdmin
from server.api.routers.admin.views.payment_history_admin import PaymentHistoryAdmin
from server.api.routers.admin.views.prohibited_phone_sites_admin import ProhibitedPhoneSitesAdmin
from server.api.routers.admin.views.prohibited_sites_admin import ProhibitedSitesAdmin
from server.api.routers.admin.views.queries_balance_admin import QueriesBalanceAdmin
from server.api.routers.admin.views.services_balance_admin import ServicesBalanceAdmin
from server.api.routers.admin.views.telegram_notifications_admin import TelegramNotificationsAdmin
from server.api.routers.admin.views.text_data_admin import TextDataAdmin
from server.api.routers.admin.views.user_balances_admin import UserBalancesAdmin
from server.api.routers.admin.views.user_queries_admin import UserQueriesAdmin
from server.api.routers.admin.views.user_role_admin import UserRoleAdmin
from server.api.routers.admin.views.users_admin import UsersAdmin

__all__ = ['BalanceHistoryAdmin', 'EventsAdmin', 'KeywordsAdmin', 'PaymentHistoryAdmin',
           'ProhibitedPhoneSitesAdmin', 'ProhibitedSitesAdmin', 'QueriesBalanceAdmin', 'ServicesBalanceAdmin',
           'TelegramNotificationsAdmin', 'TextDataAdmin', 'UserBalancesAdmin', 'UserQueriesAdmin',
           'UserRoleAdmin', 'UsersAdmin']
