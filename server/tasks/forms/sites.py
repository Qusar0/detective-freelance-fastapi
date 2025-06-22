from server.tasks.celery_config import SEARCH_ENGINES
from server.tasks.forms.forms import form_phone_number


def form_page_query(url, page_num):
    return f'{url}&page={page_num}'


def form_yandex_query_num(num: str, page_num):
    phone_num = num.replace("+", "%2B")
    url = SEARCH_ENGINES['yandex'] + f'{phone_num}&page={page_num}'
    return url


def form_yandex_query_email(email: str, page_num):
    url = SEARCH_ENGINES['yandex'] + f'"{email}"&page={page_num}'
    return url


def form_google_query(phone_num: str):
    search_keys = []
    query_variants = form_phone_number(phone_num)
    for query in query_variants:
        search_key = SEARCH_ENGINES['google'] + f'''{query}'''
        search_keys.append(search_key)

    return search_keys
