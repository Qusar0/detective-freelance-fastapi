from sqladmin import ModelView

from server.api.models import (
    PaymentHistory)


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

    column_formatters = {
        PaymentHistory.payment_amount: lambda m, a: f"{m.payment_amount:,.2f}".replace(",", " ").replace(".", ",")
    }
