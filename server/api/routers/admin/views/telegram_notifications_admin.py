from sqladmin import ModelView

from server.api.models import (
    TelegramNotifications)


class TelegramNotificationsAdmin(ModelView, model=TelegramNotifications):
    name = "Телеграм уведомления"
    name_plural = "Телеграм уведомления"
    icon = "fa-solid fa-user"

    column_list = [
        TelegramNotifications.id,
        TelegramNotifications.user,
        TelegramNotifications.chat_id
    ]
    column_labels = {
        TelegramNotifications.id: "ID",
        TelegramNotifications.user: "Пользователь",
        TelegramNotifications.chat_id: "ID чата"
    }
    column_details_exclude_list = [TelegramNotifications.user_id]
    column_searchable_list = [TelegramNotifications.chat_id]
    column_sortable_list = [TelegramNotifications.id]
