from sqladmin import ModelView

from server.api.models import (
    TextData)


class TextDataAdmin(ModelView, model=TextData):
    name = "Текстовые данные"
    name_plural = "Текстовые данные"
    icon = "fa-solid fa-file-lines"

    column_list = [
        TextData.id,
        TextData.query,
        TextData.file_path
    ]
    column_labels = {
        TextData.id: "ID",
        TextData.query: "Запрос",
        TextData.file_path: "Путь к файлу"
    }
    column_details_exclude_list = [TextData.query_id]
    column_searchable_list = [TextData.file_path]
    column_sortable_list = [TextData.id]
    can_delete = False
    can_edit = False
    can_create = False
