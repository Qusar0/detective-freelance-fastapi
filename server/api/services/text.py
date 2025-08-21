from typing import Dict, List, Any
from deep_translator import GoogleTranslator


def process_text(text: str, lang: str) -> str:
    """Обрабатывает и переводит текст с приведением к правильному регистру"""
    if not text:
        return ''
    translated = translate_text(text, 'ru', lang)[0]
    return translated.replace("-", " ").title().replace(" ", "-")


def process_keywords(keywords: List[str], lang: str) -> List[str]:
    """Переводит список ключевых слов"""
    return translate_words({"keywords": keywords}, [lang])


def process_special_field(text: str, prefix: str, lang: str) -> str:
    """Обрабатывает специальные поля (plus/minus) с разделителями"""
    if not text:
        return ''
    terms = text[len(prefix):].split(prefix)
    translated_terms = [translate_text(term, 'ru', lang)[0] for term in terms if term]
    return prefix + prefix.join(translated_terms) if translated_terms else ''


async def translate_name_fields(data: Dict[str, Any], target_languages: List[str]) -> Dict[str, Any]:
    """Переводит все текстовые поля на указанные языки"""
    translated = {
        "name": {},
        "surname": {},
        "patronymic": {},
        "plus": {},
        "minus": {},
        "keywords": {}
    }
    for lang in target_languages:
        translated["name"][lang] = process_text(data["name"], lang)
        translated["surname"][lang] = process_text(data["surname"], lang)
        translated["patronymic"][lang] = process_text(data["patronymic"], lang)

        translated["plus"][lang] = process_special_field(data["plus"], '+', lang)
        translated["minus"][lang] = process_special_field(data["minus"], '+-', lang)

        translated["keywords"][lang] = process_keywords(data["keywords"], lang)[lang]

    translated["name"]['original'] = data["name"]
    translated["surname"]['original'] = data["surname"]
    translated["patronymic"]['original'] = data["patronymic"]
    translated["plus"]['original'] = data["plus"]
    translated["minus"]['original'] = data["minus"]
    translated["keywords"]['original'] = data["keywords"]

    return translated


async def translate_company_fields(data: Dict[str, Any], target_languages: List[str]) -> Dict[str, Any]:
    """Переводит поля для поиска компании на указанные языки"""
    translated = {
        "location": {},
        "keywords": {},
        "plus": {},
        "minus": {}
    }

    for lang in target_languages:
        translated["location"][lang] = process_text(data["location"], lang)

        translated["keywords"][lang] = process_keywords(data["keywords"], lang)[lang]

        translated["plus"][lang] = process_special_field(data["plus"], '+', lang)

        translated["minus"][lang] = process_special_field(data["minus"], '+-', lang)

    translated["location"]['original'] = data["location"]
    translated["keywords"]['original'] = data["keywords"]
    translated["plus"]['original'] = data["plus"]
    translated["minus"]['original'] = data["minus"]

    return translated


def translate_text(text: str, source_lang: str, target_lang: str) -> List[str]:
    """Функция для перевода текста с разделением по точкам"""
    try:
        translated = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
        return list([word.strip().lower() for word in translated.split('. ') if word.strip()])
    except Exception as e:
        print(f"Translation error for '{text}' to '{target_lang}': {e}")
        return []


def translate_words(
    keywords_by_category: Dict[str, List[str]],
    target_languages: List[str],
    source_language: str = 'ru',
) -> Dict[str, List[str]]:
    translations = {'original': keywords_by_category}
    if not target_languages:
        target_languages = ['ru']

    for lang in target_languages:
        translations[lang] = {}
        for category, words in keywords_by_category.items():
            text_to_translate = '. '.join(words)

            translated_words = translate_text(text_to_translate, source_language, lang)
            translations[lang][category] = list(translated_words)

    return translations
