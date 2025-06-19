from sqladmin import ModelView

from server.api.models.models import BalanceHistory


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
