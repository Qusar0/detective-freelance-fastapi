from sqladmin import ModelView

from server.api.models.models import Keywords


class KeywordsAdmin(ModelView, model=Keywords):
    name = "Ключевое слово"
    name_plural = "Ключевые слова"
    icon = "fa-solid fa-key"

    column_list = [Keywords.id, Keywords.word, Keywords.keyword_type]
    column_labels = {
        Keywords.id: "ID",
        Keywords.word: "Слово",
        Keywords.keyword_type: "Тип слова"
    }
    column_searchable_list = [Keywords.word, Keywords.keyword_type]
    column_sortable_list = [Keywords.id, Keywords.word]
