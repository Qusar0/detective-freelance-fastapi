from sqladmin import ModelView

from server.api.models.models import ServicesBalance


class ServicesBalanceAdmin(ModelView, model=ServicesBalance):
    name = "Баланс сервиса"
    name_plural = "Балансы сервисов"
    icon = "fa-solid fa-server"

    column_list = [
        ServicesBalance.id,
        ServicesBalance.service_name,
        ServicesBalance.balance,
        ServicesBalance.balance_threshold,
    ]
    column_labels = {
        ServicesBalance.id: "ID",
        ServicesBalance.service_name: "Название сервиса",
        ServicesBalance.balance: "Баланс",
        ServicesBalance.balance_threshold: "Лимит для уведомлений"
    }
    column_searchable_list = [ServicesBalance.service_name]
    column_sortable_list = [ServicesBalance.id, ServicesBalance.balance]
    column_formatters = {
        ServicesBalance.balance: lambda m, a: f"{m.balance:,.2f}".replace(",", " ").replace(".", ",")
    }
