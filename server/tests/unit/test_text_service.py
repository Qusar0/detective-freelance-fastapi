from unittest.mock import patch, MagicMock

from server.api.services.text import (
    process_text,
    translate_text,
    translate_words,
)


def test_translate_text_returns_list():
    """Переведённый текст разбивается по '. ' и возвращается как список."""
    mock_translator = MagicMock()
    mock_translator.return_value.translate.return_value = "hello. world"
    with patch("server.api.services.text.GoogleTranslator", mock_translator):
        result = translate_text("привет. мир", "ru", "en")
    assert result == ["hello", "world"]


def test_translate_text_empty_string():
    """Пустая строка - GoogleTranslator не вызывается, возвращается []."""
    mock_translator = MagicMock()
    mock_translator.return_value.translate.return_value = ""
    with patch("server.api.services.text.GoogleTranslator", mock_translator):
        result = translate_text("", "ru", "en")
    assert result == []


def test_translate_text_exception_returns_empty():
    """При исключении во время перевода возвращается пустой список."""
    mock_translator = MagicMock()
    mock_translator.return_value.translate.side_effect = Exception("API error")
    with patch("server.api.services.text.GoogleTranslator", mock_translator):
        result = translate_text("привет", "ru", "en")
    assert result == []


def test_translate_text_strips_whitespace():
    """Лишние пробелы вокруг слов обрезаются."""
    mock_translator = MagicMock()
    mock_translator.return_value.translate.return_value = "  hello  "
    with patch("server.api.services.text.GoogleTranslator", mock_translator):
        result = translate_text("привет", "ru", "en")
    assert result == ["hello"]


def test_process_text_empty_returns_empty():
    """Пустая строка возвращается без изменений."""
    result = process_text("", "en")
    assert result == ""


def test_process_text_applies_title_case():
    """Результат перевода преобразуется в Title-Case."""
    mock_translator = MagicMock()
    mock_translator.return_value.translate.return_value = "ivan"
    with patch("server.api.services.text.GoogleTranslator", mock_translator):
        result = process_text("иван", "en")
    assert result == "Ivan"


def test_process_text_preserves_hyphen():
    """Дефис в имени сохраняется (пробелы заменяются обратно на дефис)."""
    mock_translator = MagicMock()
    mock_translator.return_value.translate.return_value = "ivan petrov"
    with patch("server.api.services.text.GoogleTranslator", mock_translator):
        result = process_text("иван-петров", "en")
    assert result == "Ivan-Petrov"


def test_translate_words_all_categories_translated():
    """Все категории словаря переводятся для каждого языка."""
    mock_translator = MagicMock()
    mock_translator.return_value.translate.return_value = "translated"
    with patch("server.api.services.text.GoogleTranslator", mock_translator):
        result = translate_words({"cat1": ["слово"]}, ["en"])
    assert "en" in result
    assert "cat1" in result["en"]


def test_translate_words_empty_languages_defaults_ru():
    """При пустом списке языков используется 'ru' по умолчанию."""
    mock_translator = MagicMock()
    mock_translator.return_value.translate.return_value = "слово"
    with patch("server.api.services.text.GoogleTranslator", mock_translator):
        result = translate_words({"cat": ["слово"]}, [])
    assert "ru" in result


def test_translate_words_preserves_original():
    """Ключ 'original' содержит исходный словарь без изменений."""
    mock_translator = MagicMock()
    mock_translator.return_value.translate.return_value = "translated"
    input_data = {"cat": ["слово"]}
    with patch("server.api.services.text.GoogleTranslator", mock_translator):
        result = translate_words(input_data, ["en"])
    assert result["original"] == input_data
