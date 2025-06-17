from sqladmin import ModelView

from server.api.models import (
    UserQueries)


class UserQueriesAdmin(ModelView, model=UserQueries):
    name = "Запрос пользователя"
    name_plural = "Запросы пользователей"
    icon = "fa-solid fa-magnifying-glass"

    column_list = [
        UserQueries.query_id,
        UserQueries.user,
        UserQueries.query_status,
        UserQueries.query_category,
        UserQueries.query_created_at,
        UserQueries.query_title
    ]
    column_labels = {
        UserQueries.query_id: "ID запроса",
        UserQueries.user: "Пользователь",
        UserQueries.query_status: "Статус",
        UserQueries.query_category: "Категория",
        UserQueries.query_created_at: "Дата создания",
        UserQueries.query_title: "Название",
        UserQueries.balance_histories: "История баланса",
        UserQueries.text_dates: "Расположение запроса",
        UserQueries.queries_balances: "Стоимость запроса",
        UserQueries.events: "Уведомление"
    }
    column_details_exclude_list = [
        UserQueries.user_id,
        UserQueries.query_unix_date,
        UserQueries.deleted_at,
    ]
    column_searchable_list = [
        UserQueries.query_status,
        UserQueries.query_category,
        UserQueries.query_title
    ]
    column_sortable_list = [
        UserQueries.query_id,
        UserQueries.query_created_at
    ]
