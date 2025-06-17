from sqladmin import ModelView

from server.api.models import (
    UserRole)


class UserRoleAdmin(ModelView, model=UserRole):
    name = "Роль пользователя"
    name_plural = "Роли пользователей"
    icon = "fa-solid fa-user-tag"

    column_list = [
        UserRole.id,
        UserRole.role_name,
    ]
    column_labels = {
        UserRole.id: "ID",
        UserRole.role_name: "Название роли",
    }

    column_searchable_list = [UserRole.role_name]
    column_sortable_list = [UserRole.id]
    form_columns = [UserRole.role_name]
