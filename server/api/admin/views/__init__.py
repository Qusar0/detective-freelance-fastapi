from server.api.admin.views.balance_history_admin import BalanceHistoryAdmin
from server.api.admin.views.events_admin import EventsAdmin
from server.api.admin.views.keywords_admin import KeywordsAdmin
from server.api.admin.views.payment_history_admin import PaymentHistoryAdmin
from server.api.admin.views.prohibited_phone_sites_admin import ProhibitedPhoneSitesAdmin
from server.api.admin.views.prohibited_sites_admin import ProhibitedSitesAdmin
from server.api.admin.views.queries_balance_admin import QueriesBalanceAdmin
from server.api.admin.views.services_balance_admin import ServicesBalanceAdmin
from server.api.admin.views.telegram_notifications_admin import TelegramNotificationsAdmin
from server.api.admin.views.text_data_admin import TextDataAdmin
from server.api.admin.views.user_balances_admin import UserBalancesAdmin
from server.api.admin.views.user_queries_admin import UserQueriesAdmin
from server.api.admin.views.user_role_admin import UserRoleAdmin
from server.api.admin.views.users_admin import UsersAdmin

__all__ = [
    'BalanceHistoryAdmin', 'EventsAdmin', 'KeywordsAdmin', 'PaymentHistoryAdmin',
    'ProhibitedPhoneSitesAdmin', 'ProhibitedSitesAdmin', 'QueriesBalanceAdmin', 'ServicesBalanceAdmin',
    'TelegramNotificationsAdmin', 'TextDataAdmin', 'UserBalancesAdmin', 'UserQueriesAdmin',
    'UserRoleAdmin', 'UsersAdmin'
]
