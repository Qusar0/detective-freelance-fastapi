from sqladmin import ModelView

from server.api.models import (
    Keywords)


class KeywordsAdmin(ModelView, model=Keywords):
    name = "Ключевое слово"
    name_plural = "Ключевые слова"
    icon = "fa-solid fa-key"

    column_list = [Keywords.id, Keywords.word, Keywords.word_type]
    column_labels = {
        Keywords.id: "ID",
        Keywords.word: "Слово",
        Keywords.word_type: "Тип слова"
    }
    column_searchable_list = [Keywords.word, Keywords.word_type]
    column_sortable_list = [Keywords.id, Keywords.word]
