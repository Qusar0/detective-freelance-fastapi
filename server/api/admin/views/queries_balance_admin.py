from sqladmin import ModelView

from server.api.models.models import QueriesBalance


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
    column_formatters = {
        QueriesBalance.balance: lambda m, a: f"{m.balance:,.2f}".replace(",", " ").replace(".", ",")
    }
