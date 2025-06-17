from sqladmin import ModelView

from server.api.models import (
    Users)


class UsersAdmin(ModelView, model=Users):
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"

    column_list = [
        Users.id,
        Users.email,
        Users.is_confirmed,
        Users.user_role,
        Users.created,
        Users.last_visited,
    ]
    column_labels = {
        Users.id: "ID",
        Users.email: "Email",
        Users.is_confirmed: "Подтвержден",
        Users.user_role: "Роль",
        Users.created: "Дата создания",
        Users.user_balance: "Баланс",
        Users.user_queries: "Запросы",
        Users.payment_histories: "Пополнения",
        Users.telegram_notification: "Телеграм",
        Users.confirmation_date: "Дата подтверждения",
        Users.last_visited: "Последнее посещение",
    }
    column_details_exclude_list = [Users.user_role_id, Users.password]
    column_searchable_list = [Users.email]
    column_sortable_list = [Users.id, Users.created, Users.last_visited, Users.email]

    form_columns = [Users.user_role]
    form_args = {
        'user_role': {
            'label': 'Роль пользователя',
        }
    }

    can_create = False
