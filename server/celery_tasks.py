import datetime
import os
import re
import threading
import time
from threading import Thread
from urllib.parse import urlparse
from phonenumbers import parse, NumberParseException

import aiofiles
import httpx
import requests
import xmltodict
from recordtype import recordtype
from celery import shared_task
from typing import List
import asyncio
from pathlib import Path
from server.api.error.errors import CustomError
from server.api.scripts.lampyre_num_script import Lampyre
from server.api.scripts import lampyre_email_script
from server.api.scripts.get_contact_script import get_tags_in_getcontact
from server.api.scripts.ibhldr_script import get_interests, get_groups_ibhldr_method, get_profiles, get_phones
from server.api.scripts.tgdev_io_scripts import get_groups_tgdev_method
from server.api.scripts.utils import get_default_keywords
from server.api.scripts.html_work import response_template, response_num_template, response_email_template, response_company_template, response_tg_template
from server.api.scripts import utils, db_transactions
from server.bots.notification_bot import send_notification
from server.api.conf.celery_worker import celery_app
from server.api.database.database import async_session
from server.api.conf.config import settings


url_google = f'http://xmlriver.com/search/xml?user={settings.xml_river_user_id}&key={settings.xml_river_api_key}&query='
url_yandex = f'http://xmlriver.com/search_yandex/xml?user={settings.xml_river_user_id}&key={settings.xml_river_api_key}&groupby=10&query='

FoundInfo = recordtype("FoundInfo", "title snippet url uri weight kwd word_type kwds_list fullname soc_type doc_type")
NumberInfo = recordtype("NumberInfo", "title snippet url uri weight kwd")


def get_event_loop():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop


@shared_task(bind=True, acks_late=True)
def start_search_by_name(self, search_filters):
    loop = get_event_loop()
    loop.run_until_complete(_start_search_by_name_async(search_filters))


async def _start_search_by_name_async(search_filters):
    print(f"STARTED search_by_name {search_filters[0]}")
    threads: List[Thread] = []
    all_found_info: List[FoundInfo] = []
    request_input_pack: List[tuple] = []
    urls = []

    search_name = search_filters[0]
    search_surname = search_filters[1]
    search_patronymic = search_filters[2]
    search_plus = search_filters[3]
    search_minus = search_filters[4]
    keywords_from_user = search_filters[5]
    default_keywords_type = search_filters[6]
    query_id = search_filters[7]
    price = search_filters[8]
    use_yandex = search_filters[9]
    languages = search_filters[10] if len(search_filters) > 10 else None

    async with async_session() as db:
        user_query = await db_transactions.get_user_query(query_id, db)
        if user_query.query_status == "done":
            return

        try:
            prohibited_sites_list = await utils.add_sites_from_db([], db)
            keywords: dict = await get_default_keywords(
                db,
                default_keywords_type,
            )

            keywords_from_db = keywords[1]
            len_keywords_from_user = len(keywords_from_user)
            len_keywords_from_db = len(keywords_from_db)

            if search_patronymic == "":
                full_name = [search_name, search_surname]
            else:
                full_name = [search_name, search_surname, search_patronymic]
            full_name_length = len(full_name)
            name_cases = await form_name_cases(full_name)
            for name_case in name_cases:
                search_keys = form_search_key(
                    name_case,
                    len_keywords_from_user,
                )
                for search_key in search_keys:
                    if len_keywords_from_user == 0 and len_keywords_from_db == 0:
                        generation_type = "standard"
                        form_input_pack(
                            request_input_pack, search_key,
                            "", "free word",
                            name_case, search_plus,
                            search_minus, generation_type,
                            full_name_length, url_google,
                        )
                        if use_yandex:
                            form_input_pack(
                                request_input_pack, search_key,
                                "", "free word",
                                name_case, search_plus,
                                search_minus, generation_type,
                                full_name_length, url_yandex,
                            )
                    else:
                        for kwd_from_user in keywords_from_user:
                            generation_type = "standard"
                            form_input_pack(
                                request_input_pack, search_key,
                                kwd_from_user, "free word",
                                name_case, search_plus,
                                search_minus, generation_type,
                                full_name_length, url_google,
                            )
                            if use_yandex:
                                form_input_pack(
                                    request_input_pack, search_key,
                                    kwd_from_user, "free word",
                                    name_case, search_plus,
                                    search_minus, generation_type,
                                    full_name_length, url_yandex,
                                )
                        for words_type, words in keywords_from_db.items():
                            for kwd_from_db in words:
                                generation_type = "system_keywords"
                                form_input_pack(
                                    request_input_pack, search_key,
                                    kwd_from_db, words_type,
                                    name_case, search_plus,
                                    search_minus, generation_type,
                                    full_name_length, url_google,
                                )
                                if use_yandex:
                                    form_input_pack(
                                        request_input_pack, search_key,
                                        kwd_from_db, words_type,
                                        name_case, search_plus,
                                        search_minus, generation_type,
                                        full_name_length, url_yandex,
                                    )

            for input_data in request_input_pack:
                url = input_data[0]
                urls.append(url)
                keyword = input_data[1]
                keyword_type = input_data[2]
                name_case = input_data[3]

                threads.append(Thread(
                    target=do_request_to_xmlriver,
                    args=(
                        url, all_found_info,
                        prohibited_sites_list, keyword,
                        name_case, keyword_type
                    )
                ))

            manage_threads(threads)

            titles = form_titles(
                full_name,
                default_keywords_type,
                keywords_from_user,
                search_minus,
                search_plus,
            )

            items, filters, fullname_counters = form_response_html(
                all_found_info,
            )

            html = response_template(titles, items, filters, fullname_counters)
            await db_transactions.save_html(html, query_id, db)
        except Exception as e:
            print(e)
            channel = await utils.generate_sse_message_type(
                user_id=user_query.user_id,
                db=db,
            )
            await db_transactions.change_query_status(user_query, "failed", db)
            await db_transactions.send_sse_notification(user_query, channel, db)
            await db_transactions.return_balance(
                user_query.user_id,
                user_query.query_id,
                price,
                channel,
                db,
            )

            await write_urls(urls, "name")
            await utils.renew_xml_balance(db)

            return {
                "query_id": user_query.query_id,
                "query_status": user_query.query_status,
            }

        await write_urls(urls, "name")
        await utils.renew_xml_balance(db)

        channel = await utils.generate_sse_message_type(
            user_id=user_query.user_id,
            db=db,
        )
        await db_transactions.change_query_status(user_query, "done", db)
        await db_transactions.send_sse_notification(user_query, channel, db)

        chat_id = await utils.is_user_subscribed_on_tg(user_query.user_id, db)
        if chat_id:
            await send_notification(chat_id, user_query.query_title.title())

        return {
            "query_id": user_query.query_id,
            "query_status": user_query.query_status,
        }


async def write_urls(urls, type):
    log_dir = './app/url_logs'
    os.makedirs(log_dir, exist_ok=True)

    filename = f'{log_dir}/{type}-{datetime.datetime.now()}.txt'
    async with aiofiles.open(filename, 'w') as f:
        for url in urls:
            await f.write(url + '\n')


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


async def form_name_cases(full_name: List[str]) -> List[List[str]]:
    url = "https://ws3.morpher.ru/russian/declension"
    token = "cfce1037-064f-425c-b40a-593875653972"
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
            cases.update([data['Р'], data['Д'], data['В'], data['Т'], data['П']])
        except (httpx.HTTPError, KeyError):
            pass

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
            input_pack.append((url, keyword, keyword_type, name_case))
        else:
            if generation_type == "standard":
                url += f"{plus_words}{minus_words}"
                input_pack.append((url, keyword, keyword_type, name_case))
            elif generation_type == "system_keywords" and length > 1:
                url += f"{plus_words}{minus_words}"
                input_pack.append((url, keyword, keyword_type, name_case))
            else:
                pass

    except Exception as e:
        print("form_input_pack function Exception {0}".format(e))


def do_request_to_xmlriver(
    url,
    all_found_data,
    prohibited_sites,
    keyword,
    name_case,
    keyword_type,
):
    response = requests.get(url)
    handle_xmlriver_response(
        url,
        response,
        all_found_data,
        prohibited_sites,
        keyword,
        name_case,
        keyword_type,
    )


def handle_xmlriver_response(
    url,
    response,
    all_found_data: List,
    prohibited_sites: List,
    keyword: str,
    name_case=None,
    keyword_type=None,
):
    soc_urls = {
        'vk.com': 'Вконтакте',
        'ok.ru': 'Одноклассники',
        'www.facebook.com': 'Facebook',
        'www.instagram.com': 'Instagram',
        't.me': 'Telegram',
    }
    doc_urls = {
        '.doc': 'Word',
        '.docx': 'Word',
        '.odf': 'Word',
        '.pdf': 'PDF',
        '.xls': 'Excel',
        '.xslx': 'Excel',
        '.csv': 'Excel',
        '.ods': 'Excel',
        '.txt': 'Txt',
        '.rtf': 'Txt',
        '.ppt': 'PowerPoint',
        '.pptx': 'PowerPoint',
    }

    decoded_resp = response.content.decode('utf-8')
    json_var = xmltodict.parse(decoded_resp)
    try:
        data = json_var["yandexsearch"]["response"]["results"]["grouping"]["group"]
    except KeyError:
        error = xml_errors_handler(json_var)
        return error
    try:
        if json_var['yandexsearch']['response']['fixtype'] == 'quotes':
            return '15'
    except Exception:
        pass

    if isinstance(data, dict):
        data = [data]

    for index in range(len(data) - 1):
        info_title = data[index]["doc"]["title"]
        try:
            info_snippet = data[index]["doc"]["fullsnippet"]
        except Exception:
            info_snippet = data[index]["doc"]["passages"]["passage"]

        site_uri = data[index]["doc"]["url"]
        site_url = urlparse(site_uri).netloc
        soc_type = ""
        doc_type = ""

        parsed_url = urlparse(site_uri)
        path = parsed_url.path
        file_extension = os.path.splitext(path)[1].lower()

        for key, value in soc_urls.items():
            if site_url == key:
                soc_type = value

        for key, value in doc_urls.items():
            if key == file_extension:
                doc_type = value

        if info_snippet is None:
            info_snippet = ''

        if name_case is not None:
            colored_snippet = color_keywords(name_case, info_snippet, keyword)

        banned_site_status = False
        for site in prohibited_sites:
            if site.lower() in site_url.lower() or site_uri.lower() in site.lower():
                banned_site_status = True
                break

        if not banned_site_status:
            try:
                if name_case is None and keyword_type != '':
                    all_found_data.append(
                        FoundInfo(
                            info_title.replace("`", "'").replace("\\", "\\\\"),
                            info_snippet.replace("`", "'").replace("\\", "\\\\"),
                            site_url, site_uri, 1, keyword, keyword_type,
                            [keyword],
                            'true',
                            soc_type,
                            doc_type,
                        ),
                    )
                elif name_case is None and not keyword_type:
                    all_found_data.append(
                        NumberInfo(
                            info_title.replace("`", "'"),
                            info_snippet.replace("`", "'").replace("\\", "\\\\"),
                            site_url,
                            site_uri,
                            1,
                            keyword,
                        ),
                    )
                else:
                    try:
                        if name_case[2].lower() in info_snippet.lower():
                            fullname_type = "true"
                        else:
                            fullname_type = "false"
                    except IndexError:
                        fullname_type = "false"

                    all_found_data.append(
                        FoundInfo(
                            info_title.replace("`", "'").replace("\\", "\\\\"),
                            colored_snippet.replace("`", "'").replace("\\", "\\\\"),
                            site_url,
                            site_uri,
                            1,
                            keyword,
                            keyword_type,
                            [keyword],
                            fullname_type,
                            soc_type,
                            doc_type,
                        ),
                    )
            except AttributeError:
                print(
                    "Ошибка при создании recordtype",
                    info_title,
                    info_snippet,
                )


def xml_errors_handler(xml_response):
    try:
        error_data = xml_response["yandexsearch"]["response"]["error"]
        error_code = error_data["@code"]
        error_text = error_data["#text"]
        print(error_text)
        print(error_code)

    except KeyError:
        print(xml_response)
        raise CustomError("XMLriver на обновлении.")

    if error_code == '101' and error_text == 'Сервис сбора данных на обновлении. Попробуйте чуть позже.':
        raise CustomError("XMLriver на обновлении.")

    return error_code


def color_keywords(name_case: List[str], snippet: str, keyword: str) -> str:
    if snippet is None:
        return
    name = name_case[0]
    surname = name_case[1]

    if len(name_case) == 2:
        patronymic = ""
    else:
        patronymic = name_case[2]

    keywords_list = [name, surname, patronymic, keyword]

    words = snippet.split()

    for i in range(len(words)):
        for keyword in keywords_list:
            if words[i].lower().strip(".,!?") == keyword.lower():
                words[i] = f'<span class="key-word">{words[i]}</span>'

    marked_snippet = " ".join(words)
    colored_snippet = re.sub(keyword, f'<span class="key-word">{keyword}</span>', marked_snippet, flags=re.IGNORECASE)

    return colored_snippet


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


def manage_threads(threads):
    active_threads = []
    max_threads = 20

    for thread in threads:
        # Если достигнуто максимальное количество потоков, ждем, пока хотя бы один завершится
        while threading.active_count() >= max_threads:
            time.sleep(0.1)
        thread.start()
        active_threads.append(thread)

    for thread in active_threads:
        thread.join()


def form_response_html(found_info_test) -> str:
    keywords_from_user = []
    all_js_objs, main_js_objs, free_js_objs, negative_js_objs, reputation_js_objs, relations_js_objs, soc_js_objs, doc_js_objs = "", "", "", "", "", "", "", ""

    neg_kwds, rep_kwds, rel_kwds, soc_kwds, doc_kwds = [], [], [], [], []

    filtered_data = filter_by_weight(found_info_test, "name")

    # простые счетчики категории
    main_c, free_c, neg_c, rep_c, rel_c, soc_c, doc_c = 0, 0, 0, 0, 0, 0, 0
    # счетики при ФИО для разных категории
    all_fio_c, free_fio_c, main_fio_c, neg_fio_c, rep_fio_c, rel_fio_c, soc_fio_c, doc_fio_c = 0, 0, 0, 0, 0, 0, 0, 0
    # счетики при ФИ для разных категории
    all_fi_c, free_fi_c, main_fi_c, neg_fi_c, rep_fi_c, rel_fi_c, soc_fi_c, doc_fi_c = 0, 0, 0, 0, 0, 0, 0, 0

    for i in range(len(filtered_data)):
        info: FoundInfo = filtered_data[i]
        title = info.title
        snippet = info.snippet
        uri = info.uri
        weight = info.weight
        keyword_type = info.word_type.replace("company_", "")
        keywords_list = info.kwds_list
        kwd = info.kwd
        soc_type = info.soc_type
        doc_type = info.doc_type
        fullname = info.fullname

        one_info = form_js_data(title, snippet, uri, keywords_list, fullname)

        all_js_objs += one_info
        if fullname == 'true':
            all_fio_c += 1
        else:
            all_fi_c += 1

        if weight >= 3:
            main_js_objs += one_info
            main_c += 1
            if fullname == 'true':
                main_fio_c += 1
            else:
                main_fi_c += 1

        match keyword_type:
            case "free word":
                free_js_objs += form_js_data(title, snippet, uri, keywords_list, fullname)
                if kwd not in keywords_from_user:
                    keywords_from_user.append(kwd)

                free_c += 1
                if fullname == 'true':
                    free_fio_c += 1
                else:
                    free_fi_c += 1

            case "negativ":
                negative_js_objs += form_js_data(title, snippet, uri, keywords_list, fullname)
                neg_kwds.append(kwd)

                neg_c += 1
                if fullname == 'true':
                    neg_fio_c += 1
                else:
                    neg_fi_c += 1

            case "reputation":
                reputation_js_objs += form_js_data(title, snippet, uri, keywords_list, fullname)
                rep_kwds.append(kwd)

                rep_c += 1
                if fullname == 'true':
                    rep_fio_c += 1
                else:
                    rep_fi_c += 1

            case "relations":
                relations_js_objs += form_js_data(title, snippet, uri, keywords_list, fullname)
                rel_kwds.append(kwd)

                rel_c += 1
                if fullname == 'true':
                    rel_fio_c += 1
                else:
                    rel_fi_c += 1

        if soc_type:
            soc_js_objs += form_js_data(title, snippet, uri, keywords_list, fullname, social_type=soc_type)
            soc_kwds.append(kwd)

            soc_c += 1
            if fullname == 'true':
                soc_fio_c += 1
            else:
                soc_fi_c += 1

        if doc_type:
            doc_js_objs += form_js_data(title, snippet, uri, keywords_list, fullname, doc_type=doc_type)
            doc_kwds.append(kwd)

            doc_c += 1
            if fullname == 'true':
                doc_fio_c += 1
            else:
                doc_fi_c += 1

    filters = form_var_filters(
        keywords_from_user,
        neg_kwds,
        rep_kwds,
        rel_kwds,
        soc_kwds,
        doc_kwds,
    )
    items = form_var_items(
        all_js_objs,
        main_js_objs,
        free_js_objs,
        negative_js_objs,
        reputation_js_objs,
        relations_js_objs,
        soc_js_objs,
        doc_js_objs,
    )

    fullname_counters = {
        "main": [
            main_c,
            main_fio_c,
            main_fi_c,
        ],
        "arbitrary": [
            free_c,
            free_fio_c,
            free_fi_c,
        ],
        "negative": [
            neg_c,
            neg_fio_c,
            neg_fi_c,
        ],
        "connections": [
            rel_c,
            rel_fio_c,
            rel_fi_c,
        ],
        "socials": [
            soc_c,
            soc_fio_c,
            soc_fi_c,
        ],
        "reputation": [
            rep_c,
            rep_fio_c,
            rep_fi_c,
        ],
        "documents": [
            doc_c,
            doc_fio_c,
            doc_fi_c,
        ],
        "all_materials": [
            len(filtered_data),
            all_fio_c,
            all_fi_c,
        ],
    }

    return items, filters, fullname_counters


def form_var_items(
    all_obj="",
    main="",
    free="",
    negative="",
    reputation="",
    relations="",
    socials="",
    documents="",
):
    items = {
        "all": all_obj,
        "main": main,
        "free": free,
        "negative": negative,
        "reputation": reputation,
        "relation": relations,
        "socials": socials,
        "documents": documents
    }
    return items


def form_var_filters(
    keywords_from_user="",
    neg_kwds="",
    rep_kwds="",
    rel_kwds="",
    soc_kwds="",
    doc_kwds="",
):
    kwds_objects, neg_objects, rep_objects, rel_objects, soc_objects, doc_objects = "", "", "", "", "", ""

    for kwd in keywords_from_user:
        kwds_objects += f"'{kwd}': true,\n"

    for neg_kwd in list(set(neg_kwds)):
        neg_objects += f"'{neg_kwd}': true,\n"

    for rep_kwd in list(set(rep_kwds)):
        rep_objects += f"'{rep_kwd}': true,\n"

    for rel_kwd in list(set(rel_kwds)):
        rel_objects += f"'{rel_kwd}': true,\n"

    for soc_kwd in list(set(soc_kwds)):
        soc_objects += f"'{soc_kwd}': true,\n"

    for doc_kwd in list(set(doc_kwds)):
        doc_objects += f"'{doc_kwd}': true,\n"

    filters = {
        "free_kwds": kwds_objects,
        "neg_kwds": neg_objects,
        "rep_kwds": rep_objects,
        "rel_kwds": rel_objects,
        "soc_kwds": soc_objects,
        "doc_kwds": doc_objects,
    }

    return filters


@shared_task(bind=True, acks_late=True)
def start_search_by_num(self, phone_num, methods_type, query_id, use_yandex=False):
    loop = get_event_loop()
    loop.run_until_complete(_start_search_by_num_async(phone_num, methods_type, query_id, use_yandex))


async def _start_search_by_num_async(phone_num, methods_type, query_id, use_yandex):
    print(f"start search num {phone_num}")
    _, items, filters, lampyre_html, leaks_html, acc_search_html = '', '', '', '', '', ''
    _, tags = [], []
    filters = {"free_kwds": ""}
    items = {"all": ""}

    money_to_return = 0

    async with async_session() as db:
        user_query = await db_transactions.get_user_query(query_id, db)

        if user_query.query_status == "done":
            return

        if 'mentions' in methods_type:
            try:
                items, filters = await xmlriver_num_do_request(
                    phone_num,
                    use_yandex,
                )
                await utils.renew_xml_balance(db)
            except Exception as e:
                money_to_return += 5
                print(e)
                pass
        if 'bindings' in methods_type:
            try:
                lampyre_html = lampyre_num_do_request(phone_num)
                await utils.renew_lampyre_balance(db)
            except Exception as e:
                money_to_return += 65
                print(e)
                pass

        if 'tags' in methods_type:
            try:
                tags, requests_getcontact_left = get_tags_in_getcontact(phone_num)
                await utils.renew_getcontact_balance(requests_getcontact_left, db)
            except Exception as e:
                money_to_return += 25
                print(e)
                pass

        html = response_num_template(
            phone_num,
            items,
            filters,
            lampyre_html,
            leaks_html,
            tags,
            acc_search_html,
        )

        await db_transactions.save_html(html, query_id, db)
        channel = await utils.generate_sse_message_type(
            user_id=user_query.user_id,
            db=db,
        )
        await db_transactions.change_query_status(user_query, "done", db)
        await db_transactions.send_sse_notification(user_query, channel, db)
        chat_id = await utils.is_user_subscribed_on_tg(user_query.user_id, db)
        if chat_id:
            await send_notification(chat_id, user_query.query_title)

        if money_to_return > 0:
            print('Returned', money_to_return)
            await db_transactions.return_balance(
                user_query.user_id,
                user_query.query_id,
                money_to_return,
                channel,
                db,
            )


def lampyre_num_do_request(phone_num):
    lampyre_obj = Lampyre()
    lampyre_resp = lampyre_obj.main(phone_num)
    return lampyre_resp


async def xmlriver_num_do_request(phone_num, use_yandex=False):
    all_found_data = []
    urls = []
    proh_sites = read_needless_sites()

    google_urls = form_google_query(phone_num)
    for url in google_urls:
        urls.append(url)
        response = requests.get(url=url)
        handle_xmlriver_response(url, response, all_found_data, proh_sites, phone_num)

    if use_yandex:
        counter = 0
        while True:
            url = form_yandex_query_num(phone_num, page_num=counter)
            urls.append(url)
            response = requests.get(url=url)
            handling_resp = handle_xmlriver_response(url, response, all_found_data, proh_sites, phone_num)
            if handling_resp in ('15', '110', '500'):
                break
            else:
                counter += 1

    items, filters = form_number_response_html(all_found_data, phone_num)
    await write_urls(urls, "number")
    return items, filters


def form_yandex_query_num(num: str, page_num):
    phone_num = num.replace("+", "%2B")
    url = url_yandex + f'{phone_num}&page={page_num}'
    return url


def form_google_query(phone_num: str):
    search_keys = []
    query_variants = format_phone_number(phone_num)
    for query in query_variants:
        search_key = url_google + f'''{query}'''
        search_keys.append(search_key)

    return search_keys


def format_phone_number(raw_number: str):
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


def form_yandex_query_email(email: str, page_num):
    url = url_yandex + f'"{email}"&page={page_num}'
    return url


def read_needless_sites():
    file_path = Path(__file__).parent / "phone minus sites.txt"
    print(file_path)
    with file_path.open("r", encoding="utf-8") as f:
        sites = f.readlines()
    minus_sites = [i.strip() for i in sites]
    return minus_sites


def form_number_response_html(all_found_data, phone_num):
    all_js_objs = ""
    filtered_data = filter_by_weight(all_found_data, "number")

    for i in range(len(filtered_data)):
        info: NumberInfo = filtered_data[i]
        title = info.title
        snippet = info.snippet
        uri = info.uri
        one_info = form_js_data(title, snippet, uri, [phone_num])

        all_js_objs += one_info

    filters = form_var_filters(keywords_from_user=[phone_num])
    items = form_var_items(all_obj=all_js_objs)

    return items, filters


async def xmlriver_email_do_request(email, use_yandex=False):
    all_found_data = []
    urls = []
    proh_sites = read_needless_sites()

    url = url_google + f'''"{email}"'''
    urls.append(url)

    async with httpx.AsyncClient() as client:
        response = await client.get(url=url)
        handle_xmlriver_response(url, response, all_found_data, [], email)

        if use_yandex:
            counter = 0
            while True:
                url = form_yandex_query_email(email, page_num=counter)
                urls.append(url)

                response = await client.get(url=url)
                handling_resp = handle_xmlriver_response(url, response, all_found_data, proh_sites, email)

                if handling_resp in ('15', '110', '500'):
                    break
                else:
                    counter += 1

    items, filters = form_number_response_html(all_found_data, email)

    await write_urls(urls, "email")
    return items, filters


@shared_task(bind=True, acks_late=True)
def start_search_by_email(
    self,
    email,
    methods_type,
    query_id,
    use_yandex=False,
):
    loop = get_event_loop()
    loop.run_until_complete(
        _start_search_by_email_async(
            email,
            methods_type,
            query_id,
            use_yandex,
        ),
    )


async def _start_search_by_email_async(email, methods_type, query_id, use_yandex):
    print(f"start search email {email}")
    mentions_html, leaks_html, acc_search_html, fitness_tracker, acc_checker = '', '', '', '', ''
    filters = {"free_kwds": ""}
    mentions_html = {"all": ""}

    money_to_return = 0

    async with async_session() as db:
        user_query = await db_transactions.get_user_query(query_id, db)

        if user_query.query_status == "done":
            return

        if 'mentions' in methods_type:
            try:
                mentions_html, filters = await xmlriver_email_do_request(
                    email,
                    use_yandex,
                )
                await utils.renew_xml_balance(db)
            except Exception as e:
                money_to_return += 5
                print(e)
                pass

        if 'acc checker' in methods_type:
            try:
                lampyre_email = lampyre_email_script.LampyreMail()
                acc_checker = lampyre_email.main(email, ['acc checker'])
                await utils.renew_lampyre_balance(db)
            except Exception as e:
                money_to_return += 130
                print(e)
                pass

        html = response_email_template(
            email,
            mentions_html,
            filters,
            leaks_html,
            acc_search_html,
            fitness_tracker,
            acc_checker,
        )

        await db_transactions.save_html(html, query_id, db)
        channel = await utils.generate_sse_message_type(user_id=user_query.user_id, db=db)
        await db_transactions.change_query_status(user_query, "done", db)
        await db_transactions.send_sse_notification(user_query, channel, db)
        chat_id = await utils.is_user_subscribed_on_tg(user_query.user_id, db)
        if chat_id:
            await send_notification(chat_id, user_query.query_title)

        if money_to_return > 0:
            print('Returned', money_to_return)
            await db_transactions.return_balance(user_query.user_id, user_query.query_id, money_to_return, channel, db)


@shared_task(bind=True, acks_late=True)
def start_search_by_company(self, search_filters):
    loop = get_event_loop()
    loop.run_until_complete(_start_search_by_company_async(search_filters))


async def _start_search_by_company_async(search_filters):
    print(f"start search company {search_filters[0]}")
    threads: List[Thread] = []
    all_found_info: List[FoundInfo] = []
    request_input_pack: List[tuple] = []
    urls = []

    company_names = [search_filters[0], search_filters[1]]
    location = search_filters[2]
    keywords_from_user = search_filters[3]
    default_keywords_type = search_filters[4]
    plus_words = search_filters[5]
    minus_words = search_filters[6]
    query_id = search_filters[7]
    price = search_filters[8]
    use_yandex = search_filters[9]

    async with async_session() as db:
        user_query = await db_transactions.get_user_query(query_id, db)
        if user_query.query_status == "done":
            return

        try:
            prohibited_sites_list = await utils.add_sites_from_db([], db)
            keywords: dict = await get_default_keywords(
                db,
                default_keywords_type,
            )

            keywords_from_db = keywords[1]
            len_keywords_from_user = len(keywords_from_user)
            len_keywords_from_db = len(keywords_from_db)

            for company_name in company_names:
                if company_name == '':
                    break
                if len_keywords_from_user == 0 and len_keywords_from_db == 0:
                    form_input_pack_company(request_input_pack, company_name, "", "free word", location, plus_words, minus_words, url_google)
                    if use_yandex:
                        form_input_pack_company(request_input_pack, company_name, "", "free word", location, plus_words, minus_words, url_yandex)
                else:
                    for kwd_from_user in keywords_from_user:
                        form_input_pack_company(request_input_pack, company_name, kwd_from_user, "free word", location, plus_words, minus_words, url_google)
                        if use_yandex:
                            form_input_pack_company(request_input_pack, company_name, kwd_from_user, "free word", location, plus_words, minus_words, url_yandex)

                    for words_type, words in keywords_from_db.items():
                        for kwd_from_db in words:
                            form_input_pack_company(request_input_pack, company_name, kwd_from_db, words_type, location, plus_words, minus_words, url_google)
                            if use_yandex:
                                form_input_pack_company(request_input_pack, company_name, kwd_from_db, words_type, location, plus_words, minus_words, url_yandex)

            for input_data in request_input_pack:
                url = input_data[0]
                urls.append(url)
                keyword = input_data[1]
                keyword_type = input_data[2]

                threads.append(
                    Thread(
                        target=do_request_to_xmlriver,
                        args=(
                            url,
                            all_found_info,
                            prohibited_sites_list,
                            keyword,
                            None,
                            keyword_type,
                        ),
                    ),
                )

            manage_threads(threads)

            company_titles = form_extra_titles(search_filters[1], location)
            titles = form_titles(
                search_filters[0],
                default_keywords_type,
                keywords_from_user,
                minus_words,
                plus_words,
                'company',
            )

            items, filters, fullname_counters = form_response_html(all_found_info)

            html = response_company_template(
                titles,
                items,
                filters,
                fullname_counters,
                company_titles,
            )
            await db_transactions.save_html(html, query_id, db)
        except Exception as e:
            print(e)
            channel = await utils.generate_sse_message_type(user_id=user_query.user_id, db=db)
            await db_transactions.change_query_status(user_query, "failed", db)
            await db_transactions.send_sse_notification(user_query, channel, db)
            await db_transactions.return_balance(
                user_query.user_id,
                user_query.query_id,
                price,
                channel,
                db,
            )

            await write_urls(urls, "name")
            await utils.renew_xml_balance(db)
            return {
                "query_id": user_query.query_id,
                "query_status": user_query.query_status,
            }

        await write_urls(urls, "company")
        await utils.renew_xml_balance(db)

        channel = await utils.generate_sse_message_type(user_id=user_query.user_id, db=db)
        await db_transactions.change_query_status(user_query, "done", db)
        await db_transactions.send_sse_notification(user_query, channel, db)
        chat_id = await utils.is_user_subscribed_on_tg(user_query.user_id, db)
        if chat_id:
            await send_notification(chat_id, user_query.query_title.title())

        return {
            "query_id": user_query.query_id,
            "query_status": user_query.query_status,
        }


def form_input_pack_company(
    input_pack,
    company_name: str,
    keyword: str,
    keyword_type: str,
    location,
    plus_words,
    minus_words,
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

    url += f"{plus_words}{minus_words}"
    input_pack.append((url, keyword, keyword_type))


def form_extra_titles(second_name, location):
    extra_titles = ""
    if second_name != "":
        extra_titles += f'<span class="max-text-length" title="Дополнительное наименование: {second_name}"><b>Дополнительное наименование:</b> {second_name}</span>'

    if location != "":
        extra_titles += f'<span class="max-text-length" title="Местонахождение: {location}"><b>Местонахождение:</b> {location}</span>'

    return extra_titles


@shared_task(bind=True, acks_late=True)
async def start_search_by_telegram(self, search_filters):
    username = search_filters[0]
    tg_user_id = search_filters[1]
    query_id = search_filters[2]
    _ = search_filters[3]
    methods_type = search_filters[4]

    interests_html, groups1_html, groups2_html, profiles_html, phones_html = '', '', '', '', ''

    tg_user_id = str(tg_user_id)
    user_query = db_transactions.get_user_query(query_id)
    if user_query.query_status == "done":
        return

    if 'interests' in methods_type:
        try:
            interests_html = get_interests(tg_user_id)
        except Exception as e:
            print(e)
            pass
    if 'groups_1' in methods_type:
        try:
            groups1_html = get_groups_ibhldr_method(tg_user_id)
        except Exception as e:
            print(e)
            pass
    if 'groups_2' in methods_type:
        try:
            groups2_html = get_groups_tgdev_method(tg_user_id)
        except Exception as e:
            print(e)
            pass
    if 'profile_history' in methods_type:
        try:
            profiles_html = get_profiles(tg_user_id)
        except Exception as e:
            print(e)
            pass
    if "phone_number" in methods_type:
        try:
            phones_html = get_phones(tg_user_id)
        except Exception as e:
            print(e)
            pass

    html = response_tg_template(username + "ID" + tg_user_id if username != "" else tg_user_id, interests_html, groups1_html, groups2_html, profiles_html, phones_html)

    await db_transactions.save_html(html, query_id)
    channel = await utils.generate_sse_message_type(user_id=user_query.user_id)
    await db_transactions.change_query_status(user_query, "done")
    await db_transactions.send_sse_notification(user_query, channel)
    chat_id = await utils.is_user_subscribed_on_tg(user_query.user_id)
    if chat_id:
        await send_notification(chat_id, user_query.query_title)
