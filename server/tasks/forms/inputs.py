import re

from server.tasks.celery_config import SEARCH_ENGINES


def form_input_pack_company(
    input_pack,
    company_name: str,
    keyword: str,
    keyword_type: str,
    location,
    plus_words,
    minus_words,
    lang,
    base_url: str,
):
    if company_name == f'"{company_name}"':
        url = f'''{base_url}{company_name}'''
    else:
        url = f'''{base_url}"{company_name}"'''

    if keyword != "":
        url += f"+{keyword}"
    else:
        keyword = "ключевых слов нет"

    if location != "":
        url += f"+{location}"

    url += f"{plus_words}{minus_words}&lr={lang}"
    input_pack.append((url, keyword, keyword_type, None))


def form_input_pack(
    input_pack,
    search_key: str,
    keyword: str,
    keyword_type: str,
    name_case,
    plus_words,
    minus_words,
    generation_type: str,
    full_name_length: int,
    lang: str,
    base_url: str,
):
    try:
        url = f'''{base_url}{search_key}'''
        if keyword != "":
            url += f"+{keyword}"
        else:
            keyword = "ключевых слов нет"

        pattern = r'\w\+'
        matches = re.findall(pattern, search_key)
        length = len(matches)

        if full_name_length == 2:
            url += f"{plus_words}{minus_words}"
        else:
            if generation_type == "standard":
                url += f"{plus_words}{minus_words}"
            elif generation_type == "system_keywords" and length > 1:
                url += f"{plus_words}{minus_words}"

        if base_url == SEARCH_ENGINES['google']:
            url += f"&lr={lang}"
        elif base_url == SEARCH_ENGINES['yandex']:
            url += f"&lang={lang}"

        input_pack.append((url, keyword, keyword_type, name_case))
    except Exception as e:
        print("form_input_pack function Exception {0}".format(e))
