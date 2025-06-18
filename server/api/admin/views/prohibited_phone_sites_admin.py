from sqladmin import ModelView

from server.api.models.models import ProhibitedSites, ProhibitedPhoneSites


class ProhibitedPhoneSitesAdmin(ModelView, model=ProhibitedPhoneSites):
    name = "Запрещенный сайт (телефон)"
    name_plural = "Запрещенные сайты (телефон)"
    icon = "fa-solid fa-globe"

    column_list = [ProhibitedSites.id, ProhibitedSites.site_link]
    column_labels = {
        ProhibitedSites.id: "ID",
        ProhibitedSites.site_link: "Ссылка на сайт"
    }
    column_searchable_list = [ProhibitedSites.site_link]
    column_sortable_list = [ProhibitedSites.id]
