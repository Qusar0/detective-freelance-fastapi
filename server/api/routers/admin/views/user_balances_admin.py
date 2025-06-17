from sqladmin import ModelView

from server.api.models import (
    UserBalances)


class UserBalancesAdmin(ModelView, model=UserBalances):
    name = "Баланс пользователя"
    name_plural = "Балансы пользователей"
    icon = "fa-solid fa-wallet"

    column_list = [
        UserBalances.id,
        UserBalances.user,
        UserBalances.balance
    ]
    column_labels = {
        UserBalances.id: "ID",
        UserBalances.user: "Пользователь",
        UserBalances.balance: "Баланс"
    }
    column_details_exclude_list = [UserBalances.user_id]
    column_searchable_list = []
    column_sortable_list = [UserBalances.id, UserBalances.balance]
    can_delete = False
    can_create = False
