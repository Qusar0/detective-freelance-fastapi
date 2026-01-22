from loguru import logger
import httpx
from typing import List
from phonenumbers import parse, NumberParseException

from server.api.schemas.query import FoundInfo
from server.api.conf.config import settings


def form_phone_number(raw_number: str):
    try:
        number = parse(raw_number, None)

        raw = raw_number.replace("+", "%2B")

        country_code = number.country_code
        national_number = str(number.national_number)

        operator_code_len = 3 if len(national_number) > 6 else 2
        operator_code = national_number[:operator_code_len]
        subscriber_number = national_number[operator_code_len:]

        formatted = f"%2B{country_code}%28{operator_code}%29{subscriber_number}"
        return [raw, formatted]

    except NumberParseException:
        return [raw_number]


def form_extra_titles(second_name, location):
    extra_titles = ""
    if second_name != "":
        extra_titles += f'< \
            span class="max-text-length" \
            title="Дополнительное наименование: {second_name}"> \
            <b>Дополнительное наименование:</b> {second_name}</span>'

    if location != "":
        extra_titles += f'< \
        span class="max-text-length" \
        title="Местонахождение: {location}"> \
        <b>Местонахождение:</b> {location}</span>'

    return extra_titles


def form_titles(
    fullname,
    default_kwds_name,
    keywords_from_user,
    minus_words,
    plus_words,
    type='',
):
    if isinstance(fullname, list) and len(fullname) == 3:
        fullname = f"{fullname[1]} {fullname[0]} {fullname[2]}".title()
    elif isinstance(fullname, list) and len(fullname) == 2:
        fullname = f"{fullname[1]} {fullname[0]}".title()

    possible_kwd_types = {
        'report': 'досье',
        'reputation': 'репутация',
        'negativ': 'негатив',
        'relations': 'связи',
    }

    possible_kwd_types_company = {
        'company_reputation': 'репутация',
        'company_negativ': 'негатив',
        'company_relations': 'связи',
        'company_report': 'досье'
    }

    default_kwds_rus_name = []

    if type == 'company':
        for key, value in possible_kwd_types_company.items():
            if key in default_kwds_name:
                default_kwds_rus_name.append(value)
    else:
        for key, value in possible_kwd_types.items():
            if key in default_kwds_name:
                default_kwds_rus_name.append(value)

    if default_kwds_rus_name:
        default_kwds_rus_name_str = ", ".join(default_kwds_rus_name)
    else:
        default_kwds_rus_name_str = 'Не используются'

    if keywords_from_user:
        keywords_from_user = ", ".join(keywords_from_user)
    else:
        keywords_from_user = 'Не используются'

    if minus_words:
        minus_words = minus_words.replace("+-", ",")[1:]
    else:
        minus_words = 'Не используются'

    if plus_words:
        plus_words = plus_words.replace("+", ",")[1:]
    else:
        plus_words = 'Не используются'

    titles = [
        fullname,
        default_kwds_rus_name_str,
        keywords_from_user,
        minus_words,
        plus_words,
    ]
    return titles


async def form_name_cases(full_name: List[str], language: str = None) -> List[List[str]]:
    """
    Склоняет имя используя API Морфера для указанного языка.
    Args:
        full_name: Список частей имени (имя, фамилия, отчество)
        language: Код языка ('ru', 'uk', 'kk') - если None, используется русский язык
    Returns:
        Список вариантов склонения имени
    """
    if language is None:
        language = 'ru'

    supported_languages = ['ru', 'uk', 'kk']
    if language not in supported_languages:
        logger.info(f"Язык {language} не поддерживается Морфером. Возвращаем исходные данные.")
        return [full_name]

    language_endpoints = {
        'ru': '/russian',
        'uk': '/ukrainian',
        'kk': '/qazaq'
    }
    language_cases = {
        'ru': ['Р', 'Д', 'В', 'Т', 'П'],
        'uk': ['Р', 'Д', 'З', 'О', 'М', 'K'],
        'kk': ['A', 'І', 'Б', 'Т', 'Ш', 'Ж', 'К']
    }

    url = f"https://ws3.morpher.ru{language_endpoints[language]}/declension"
    token = settings.morpher_token
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/113.0.0.0 Safari/537.36'
        )
    }

    if len(full_name) == 2:
        fio = f"{full_name[0]} {full_name[1]}"
    else:
        fio = f"{full_name[0]} {full_name[1]} {full_name[2]}"

    params = {
        "s": fio,
        "format": "json",
        "token": token
    }

    cases = set()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            cases_to_get = language_cases[language]
            for case in cases_to_get:
                if case in data:
                    cases.add(data[case])
        except (httpx.HTTPError, KeyError) as e:
            logger.error(f"Ошибка при работе с Морфером для языка {language}: {str(e)}")

    name_cases = [name.split(" ") for name in cases]
    name_cases.insert(0, full_name)

    unique_name_cases = []
    for case in name_cases:
        if case not in unique_name_cases:
            unique_name_cases.append(case)

    return unique_name_cases


def form_search_key(name_case: List[str], len_kwds_from_user) -> List[str]:
    """
    Функция для формирования запроса.
    Если юзер указал только ФИ запрос будет только по ФИ+ИФ.
    Если юзер указал ФИО составляется запрос по ФИО+ИОФ и также ФИ+ИФ
    """
    name = name_case[0]
    surname = name_case[1]

    logger.debug(f"DEBUG - name_case: {name_case}")

    if len(name_case) == 3:
        patronymic = name_case[2]
    else:
        patronymic = ""

    search_keys = []
    if patronymic == "":
        search_key1 = f'''"{surname}+{name}"'''
        search_key2 = f'''"{name}+{surname}"'''

        search_keys.extend([search_key1, search_key2])

    else:
        search_key1 = f'''"{surname}+{name}+{patronymic}"'''
        search_key2 = f'''"{name}+{patronymic}+{surname}"'''

        search_keys.extend([search_key1, search_key2])

        if len_kwds_from_user != 0:
            search_key3 = f'''"{surname}+{name}"'''
            search_key4 = f'''"{name}+{surname}"'''
            search_keys.extend([search_key3, search_key4])

    return search_keys


def form_js_data(
    title,
    snippet,
    uri,
    keyword_list,
    fullname_type="",
    social_type="",
    doc_type="",
):
    if fullname_type != "":
        js_data = f"""
        {{
                    title: `{title}`,
                    link: `{uri}`,
                    content: `{snippet}`,
                    keyword_list: {keyword_list},
                    fullname: {fullname_type},
                    social_type: `{social_type}`,
                    doc_type: `{doc_type}`
                }},
        """
    else:
        js_data = f"""
                {{
                            title: `{title}`,
                            link: `{uri}`,
                            content: `{snippet}`,
                            keyword_list: {keyword_list},
                        }},
                """
    return js_data


def filter_by_weight(all_found_info, search_type) -> List[FoundInfo]:
    def sort_key(data: FoundInfo):
        return data.weight

    for info_indx in range(len(all_found_info)):
        counter = 0
        for inner_info_indx in range(info_indx + 1, len(all_found_info)):
            inner_info_indx -= counter
            if all_found_info[info_indx].uri == all_found_info[inner_info_indx].uri:
                if search_type == "name":
                    all_found_info[info_indx].kwds_list = list(
                        set(
                            all_found_info[info_indx].kwds_list + all_found_info[inner_info_indx].kwds_list
                        )
                    )
                    all_found_info[info_indx].weight = len(
                        all_found_info[info_indx].kwds_list
                    )
                all_found_info.remove(
                    all_found_info[inner_info_indx]
                )
                counter += 1

    found_info_test = sorted(
        all_found_info,
        key=sort_key,
    )[::-1]
    return found_info_test
