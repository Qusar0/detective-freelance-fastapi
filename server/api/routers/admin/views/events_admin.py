from sqladmin import ModelView

from server.api.models import (
    Events)


class EventsAdmin(ModelView, model=Events):
    name = "Событие"
    name_plural = "События"
    icon = "fa-solid fa-calendar-check"

    column_list = [
        Events.event_id,
        Events.event_type,
        Events.event_status,
        Events.query,
        Events.created_time
    ]
    column_labels = {
        Events.event_id: "ID события",
        Events.event_type: "Тип события",
        Events.event_status: "Статус",
        Events.query: "Запрос",
        Events.created_time: "Время создания"
    }
    column_details_exclude_list = [Events.query_id, Events.additional_data]
    column_searchable_list = [Events.event_type, Events.event_status]
    column_sortable_list = [Events.event_id, Events.created_time]
    can_create = False
    can_edit = False
