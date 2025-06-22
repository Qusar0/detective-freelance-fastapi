import datetime
import os
import re
import threading
import time
import logging
from threading import Thread, Lock
from urllib.parse import urlparse
from phonenumbers import parse, NumberParseException
from abc import ABC, abstractmethod
from collections import defaultdict
import aiofiles
import httpx
import requests
import xmltodict
from recordtype import recordtype
from server.api.conf.celery_worker import celery_app
from celery import shared_task
from typing import List, Dict, Any, Optional, Tuple
import asyncio
from pathlib import Path
from server.api.error.errors import CustomError
from server.api.scripts.lampyre_num_script import Lampyre
from server.api.scripts import lampyre_email_script
from server.api.handlers.getcontact import GetContactService
from server.api.scripts.ibhldr_script import (
    get_interests,
    get_groups_ibhldr_method,
    get_profiles,
    get_phones,
)
from server.api.scripts.tgdev_io_scripts import get_groups_tgdev_method
from server.api.scripts.utils import (
    get_default_keywords,
    get_languages_by_code,
    get_countries_code_by_languages,
)
from server.api.scripts.html_work import (
    response_template,
    response_num_template,
    response_email_template,
    response_company_template,
    response_tg_template,
)
from server.api.scripts import utils, db_transactions
from server.bots.notification_bot import send_notification
from server.api.database.database import async_session
from server.api.conf.config import settings
from server.api.services.file_storage import FileStorageService
from server.api.scripts.db_transactions import delete_query_by_id
from server.api.models.models import ProhibitedPhoneSites
from sqlalchemy import select
from server.api.models.models import TextData


SEARCH_ENGINES = {
    'google': f'http://xmlriver.com/search/xml?user={settings.xml_river_user_id}&key={settings.xml_river_api_key}&query=',
    'yandex': f'http://xmlriver.com/search_yandex/xml?user={settings.xml_river_user_id}&key={settings.xml_river_api_key}&groupby=10&query=',
}


FoundInfo = recordtype("FoundInfo", "title snippet url uri weight kwd word_type kwds_list fullname soc_type doc_type")
NumberInfo = recordtype("NumberInfo", "title snippet url uri weight kwd")


def get_event_loop():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop


class SearchLogger:
    def __init__(self, query_id, log_file="search_errors.log"):
        self.query_id = query_id
        self.log_file = log_file
        self.lock = threading.Lock()
        
    def log_error(self, error_message):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [ID:{self.query_id}] ОШИБКА: {error_message}\n"
        
        with self.lock:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_entry)


class BaseSearchTask(ABC):
    def __init__(self, query_id: int, price: float):
        self.query_id = query_id
        self.price = price
        self.money_to_return = 0
        self.request_stats = {
            'total_requests': 0,
            'success_first_try': 0,
            'success_after_retry': defaultdict(int),
            'failed_after_max_retries': 0,
        }
        self.stats_lock = Lock()

    async def execute(self):
        async with async_session() as db:
            user_query = await db_transactions.get_user_query(self.query_id, db)
            if user_query.query_status == "done":
                return

            try:
                await self._process_search(db)
                await self._handle_success(user_query, db)
            except Exception as e:
                print(e)
                await self._handle_error(user_query, db)
            finally:
                delete_query_task.apply_async(args=[user_query.query_id], countdown=settings.query_delete_delay_seconds)
                await self._update_balances(db)

    @abstractmethod
    async def _process_search(self, db):
        pass

    async def _handle_success(self, user_query, db):
        channel = await utils.generate_sse_message_type(user_id=user_query.user_id, db=db)
        await db_transactions.change_query_status(user_query, "done", db)
        await db_transactions.send_sse_notification(user_query, channel, db)
        
        chat_id = await utils.is_user_subscribed_on_tg(user_query.user_id, db)
        if chat_id:
            await send_notification(chat_id, user_query.query_title)

    async def _handle_error(self, user_query, db):
        channel = await utils.generate_sse_message_type(user_id=user_query.user_id, db=db)
        await db_transactions.change_query_status(user_query, "failed", db)
        await db_transactions.send_sse_notification(user_query, channel, db)
        
        if self.money_to_return > 0:
            await db_transactions.return_balance(
                user_query.user_id,
                user_query.query_id,
                self.money_to_return,
                channel,
                db,
            )

    @abstractmethod 
    async def _update_balances(self, db):
        pass

    def save_stats_to_file(self, filename="search_stats.txt"):
        """Сохраняет статистику запросов в файл с русскоязычным выводом и ID запроса"""
        with self.stats_lock:
            total = self.request_stats['total_requests']
            if total == 0:
                return "Не было выполнено ни одного запроса."

            stats_text = [
                f"=== СТАТИСТИКА ЗАПРОСА ID: {self.query_id} ===",
                f"Общее количество запросов: {total}",
                f"Успешно с 1 попытки: {self.request_stats['success_first_try']} ({self.request_stats['success_first_try'] / total * 100:.1f}%)",
                *[f"Успешно после {attempt} попыток: {count} ({count / total * 100:.1f}%)" 
                for attempt, count in sorted(self.request_stats['success_after_retry'].items())],
                f"Не удалось после всех попыток: {self.request_stats['failed_after_max_retries']} ({self.request_stats['failed_after_max_retries'] / total * 100:.1f}%)",
                f"Время формирования отчета: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "===================================="
            ]
            
            with open(filename, "a", encoding="utf-8") as f:
                f.write("\n".join(stats_text) + "\n\n")


class NameSearchTask(BaseSearchTask):
    def __init__(self, search_filters: Tuple):
        super().__init__(search_filters[7], search_filters[8])
        self.search_name = search_filters[0]
        self.search_surname = search_filters[1]
        self.search_patronymic = search_filters[2]
        self.search_plus = search_filters[3]
        self.search_minus = search_filters[4]
        self.keywords_from_user = search_filters[5]
        self.default_keywords_type = search_filters[6]
        self.search_engines = search_filters[9]
        self.languages = search_filters[10] if len(search_filters) > 10 else ['ru']
        self.logger = SearchLogger(self.query_id, 'search_name.log')

    async def _process_search(self, db):        
        threads: List[Thread] = []
        all_found_info: List[FoundInfo] = []
        request_input_pack: List[tuple] = []
        urls = []

        try:
            prohibited_sites_list = await utils.add_sites_from_db([], db)
            keywords: dict = await get_default_keywords(db, self.default_keywords_type, self.languages)
            keywords_from_db = keywords[1]
            titles = []

            original_full_name = [self.search_name['original'], self.search_surname['original']]
            if self.search_patronymic['original']:
                original_full_name.append(self.search_patronymic['original'])

            for lang in self.languages:
                full_name = [self.search_name[lang], self.search_surname[lang]]
                if self.search_patronymic[lang]:
                    full_name.append(self.search_patronymic[lang])

                name_cases = await form_name_cases(full_name)
                len_keywords_from_user = len(self.keywords_from_user[lang]['keywords'])
                len_keywords_from_db = len(keywords_from_db[lang])

                await self._form_search_requests(
                    name_cases,
                    len_keywords_from_user,
                    len_keywords_from_db,
                    keywords_from_db[lang],
                    request_input_pack,
                    lang,
                )

            await self._process_search_requests(
                request_input_pack,
                threads,
                all_found_info,
                prohibited_sites_list,
                urls,
                db,
            )

            titles.extend(
                form_titles(
                    original_full_name,
                    self.default_keywords_type,
                    self.keywords_from_user['original'],
                    self.search_minus['original'],
                    self.search_plus['original'],
                ),
            )

            languages_names = await get_languages_by_code(db, self.languages)
            titles.append(languages_names)
        
            manage_threads(threads)
            self.save_stats_to_file('search_name.log')
            await write_urls(urls, "name")
            
            items, filters, fullname_counters = form_response_html(all_found_info)
            html = response_template(titles, items, filters, fullname_counters)

            file_storage = FileStorageService()

            await db_transactions.save_html(html, self.query_id, db, file_storage)

        except Exception as e:
            print(e)
            self.money_to_return = self.price
            raise e

    async def _update_balances(self, db):
        await utils.renew_xml_balance(db)

    async def _form_search_requests(
        self,
        name_cases,
        len_keywords_from_user,
        len_keywords_from_db,
        keywords_from_db,
        request_input_pack,
        lang,
    ):
        for name_case in name_cases:
            search_keys = form_search_key(name_case, len_keywords_from_user)
            for search_key in search_keys:
                if len_keywords_from_user == 0 and len_keywords_from_db == 0:
                    self._add_standard_search(
                        request_input_pack,
                        search_key,
                        name_case,
                        lang,
                    )
                else:
                    await self._add_keyword_searches(
                        request_input_pack,
                        search_key,
                        name_case,
                        keywords_from_db,
                        lang,
                    )

    def _add_standard_search(
        self,
        request_input_pack,
        search_key,
        name_case,
        lang,
    ):
        for engine in self.search_engines:
            if url := SEARCH_ENGINES.get(engine):
                form_input_pack(
                    request_input_pack,
                    search_key,
                    "",
                    "free word",
                    name_case,
                    self.search_plus[lang],
                    self.search_minus[lang],
                    "standard",
                    len(name_case),
                    lang,
                    url,
                )

    async def _add_keyword_searches(
        self,
        request_input_pack,
        search_key,
        name_case,
        keywords_from_db,
        lang,
    ):
        for kwd_from_user in self.keywords_from_user[lang]['keywords']:
            for engine in self.search_engines:
                if url := SEARCH_ENGINES.get(engine):
                    form_input_pack(
                        request_input_pack,
                        search_key,
                        kwd_from_user,
                        "free word",
                        name_case,
                        self.search_plus[lang],
                        self.search_minus[lang],
                        "standard",
                        len(name_case),
                        lang,
                        url,
                    )

        if self.search_patronymic[lang] == '' or len(search_key.split('+')) != 2:
            for words_type, words in keywords_from_db.items():
                for kwd_from_db in words:
                    for engine in self.search_engines:
                        if url := SEARCH_ENGINES.get(engine):
                            form_input_pack(
                                request_input_pack,
                                search_key,
                                kwd_from_db,
                                words_type,
                                name_case,
                                self.search_plus[lang],
                                self.search_minus[lang],
                                "system_keywords",
                                len(name_case),
                                lang,
                                url,
                            )

    async def _process_search_requests(
        self,
        request_input_pack,
        threads,
        all_found_info,
        prohibited_sites_list,
        urls,
        db,
    ):
        for input_data in request_input_pack:
            url = input_data[0]
            keyword = input_data[1]
            keyword_type = input_data[2]
            name_case = input_data[3]
            threads.append(
                Thread(
                    target=do_request_to_xmlriver,
                    args=(
                        url,
                        all_found_info,
                        prohibited_sites_list,
                        keyword,
                        name_case,
                        keyword_type,
                        urls,
                        self.request_stats,
                        self.stats_lock,
                        self.logger
                    ),
                ),
            )


@shared_task(bind=True, acks_late=True, queue='name_tasks')
def start_search_by_name(self, search_filters):
    loop = get_event_loop()
    task = NameSearchTask(search_filters)
    loop.run_until_complete(task.execute())


def update_stats(request_stats, stats_lock, attempt, success=True):
    with stats_lock:
        request_stats['total_requests'] += 1
        if success:
            if attempt == 1:
                request_stats['success_first_try'] += 1
            else:
                request_stats['success_after_retry'][attempt] += 1
        else:
            request_stats['failed_after_max_retries'] += 1


async def write_urls(urls, type):
    log_dir = './url_logs'
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

    logging.debug(f"DEBUG - name_case: {name_case}")

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


def do_request_to_xmlriver(
    url,
    all_found_data,
    prohibited_sites,
    keyword,
    name_case,
    keyword_type,
    urls,
    request_stats,
    stats_lock,
    logger : SearchLogger,
):
    max_attempts = 5
    retry_delay = 2
    if SEARCH_ENGINES['google'] in url:
        for attempt in range(1, max_attempts + 1):
            try:
                response = requests.get(url)
                handling_resp = handle_xmlriver_response(
                    url,
                    response,
                    all_found_data,
                    prohibited_sites,
                    keyword,
                    name_case,
                    keyword_type,
                )
                if handling_resp not in ('500', '110', '111'):
                    urls.append(url)
                    update_stats(request_stats, stats_lock, attempt, success=True)
                    break
                else:
                    logger.log_error(f"{handling_resp} | URL: {url} | Попытка: {attempt}")
                    if attempt < max_attempts:
                        time.sleep(retry_delay)
            except Exception as e:
                logger.log_error(f"Исключение: {str(e)} | URL: {url} | Попытка: {attempt}")
                if attempt < max_attempts:
                    time.sleep(retry_delay)
        else:
            logger.log_error(f"Запрос полностью провален: {url}")
            update_stats(request_stats, stats_lock, attempt, success=False)
    
    elif SEARCH_ENGINES['yandex'] in url:
        page_num = 0
        handling_resp = None
        
        while handling_resp not in ('15'):
            for attempt in range(1, max_attempts + 1):
                try:
                    new_url = form_page_query(url, page_num)
                    response = requests.get(new_url)
                    handling_resp = handle_xmlriver_response(
                            url,
                            response,
                            all_found_data,
                            prohibited_sites,
                            keyword,
                            name_case,
                            keyword_type,
                    )
                    if handling_resp not in ('500', '110', '111'):
                        urls.append(new_url)
                        update_stats(request_stats, stats_lock, attempt, success=True)
                        page_num += 1
                        break
                    else:
                        logging.error(f"Yandex request failed. URL: {new_url}, Status: {response.status_code}, Attempt: {attempt}")
                        if attempt < max_attempts:
                            time.sleep(retry_delay)
                except Exception as e:
                    logging.error(f"Yandex request exception. URL: {new_url}, Error: {str(e)}, Attempt: {attempt}")
                    if attempt < max_attempts:
                        time.sleep(retry_delay)
            else:
                update_stats(request_stats, stats_lock, attempt, success=False)

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
        all_obj=all_js_objs,
        main=main_js_objs,
        free=free_js_objs,
        negative=negative_js_objs,
        reputation=reputation_js_objs,
        relations=relations_js_objs,
        socials=soc_js_objs,
        documents=doc_js_objs,
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

    all_kwds = f"{kwds_objects}{neg_objects}{rep_objects}{rel_objects}{soc_objects}{doc_objects}"
    filters = {
        "free_kwds": kwds_objects,
        "neg_kwds": neg_objects,
        "rep_kwds": rep_objects,
        "rel_kwds": rel_objects,
        "soc_kwds": soc_objects,
        "doc_kwds": doc_objects,
        "all_kwds": all_kwds,
    }

    return filters


class NumberSearchTask(BaseSearchTask):
    def __init__(self, phone_num: str, methods_type: List[str], query_id: int, price: float):
        super().__init__(query_id, price)
        self.phone_num = phone_num
        self.methods_type = methods_type
        self.logger = SearchLogger(self.query_id, 'search_num.log')

    async def _process_search(self, db):
        self.requests_getcontact_left = await utils.get_service_balance(db, 'GetContact')
        items, filters = {}, {}
        lampyre_html, leaks_html, acc_search_html = '', '', ''
        tags = []
        getcontact_data = {}

        if 'mentions' in self.methods_type:
            try:
                items, filters = await self.xmlriver_num_do_request(db)
            except Exception as e:
                self.money_to_return += 5
                print(e)

        if 'tags' in self.methods_type:
            try:
                tags, self.requests_getcontact_left, getcontact_data = GetContactService.get_tags_and_data(self.phone_num)
            except Exception as e:
                self.money_to_return += 25
                print(e)
                getcontact_data = ''
        else:
            getcontact_data = ''

        html = response_num_template(
            self.phone_num,
            items,
            filters,
            lampyre_html,
            tags,
            acc_search_html,
            getcontact_data,
        )
        self.save_stats_to_file('search_num.log')
        try:
            file_storage = FileStorageService()
            await db_transactions.save_html(html, self.query_id, db, file_storage)

        except Exception as e:
            logging.error(f"{str(e)}")
            self.money_to_return = self.price
            raise e
    
    async def _update_balances(self, db):
        await utils.renew_xml_balance(db)
        await utils.renew_lampyre_balance(db)
        await utils.renew_getcontact_balance(self.requests_getcontact_left, db)

    async def xmlriver_num_do_request(self, db):
        all_found_data = []
        urls = []
        proh_sites = await read_needless_sites(db)
        max_attempts = 5
        retry_delay = 2

        # Обработка Google запросов
        google_urls = form_google_query(self.phone_num)
        for url in google_urls:
            for attempt in range(1, max_attempts + 1):
                try:
                    response = requests.get(url=url)
                    handling_resp = handle_xmlriver_response(url, response, all_found_data, proh_sites, self.phone_num)
                    
                    if handling_resp not in ('500', '110', '111'):
                        urls.append(url)
                        update_stats(self.request_stats, self.stats_lock, attempt, success=True)
                        break
                    else:
                        self.logger.log_error(f"{handling_resp} | URL: {url} | Попытка: {attempt}")
                        if attempt < max_attempts:
                            time.sleep(retry_delay)
                except Exception as e:
                    self.logger.log_error(f"Исключение: {str(e)} | URL: {url} | Попытка: {attempt}")
                    if attempt < max_attempts:
                        time.sleep(retry_delay)
            else:
                self.logger.log_error(f"Google запрос полностью провален: {url}")
                update_stats(self.request_stats, self.stats_lock, attempt, success=False)

        # Обработка Yandex запросов
        counter = 0
        while True:
            url = form_yandex_query_num(self.phone_num, page_num=counter)
            
            for attempt in range(1, max_attempts + 1):
                try:
                    response = requests.get(url=url)
                    handling_resp = handle_xmlriver_response(url, response, all_found_data, proh_sites, self.phone_num)
                    
                    if handling_resp == '15':
                        update_stats(self.request_stats, self.stats_lock, attempt, success=True)
                        urls.append(url)
                        break
                    elif handling_resp in ('500', '110', '111'):
                        self.logger.log_error(f"{handling_resp} | URL: {url} | Попытка: {attempt}")
                        if attempt < max_attempts:
                            time.sleep(retry_delay)
                    else:
                        urls.append(url)
                        update_stats(self.request_stats, self.stats_lock, attempt, success=True)
                        counter += 1
                        break
                except Exception as e:
                    self.logger.log_error(f"Исключение: {str(e)} | URL: {url} | Попытка: {attempt}")
                    if attempt < max_attempts:
                        time.sleep(retry_delay)
            else:
                self.logger.log_error(f"Yandex запрос полностью провален: {url}")
                update_stats(self.request_stats, self.stats_lock, attempt, success=False)
            
            if handling_resp == '15':
                break

        items, filters = form_number_response_html(all_found_data, self.phone_num)
        await write_urls(urls, "number")
        return items, filters

class EmailSearchTask(BaseSearchTask):
    def __init__(self, email: str, methods_type: List[str], query_id: int, price: float):
        super().__init__(query_id, price)
        self.email = email
        self.methods_type = methods_type
        self.logger = SearchLogger(self.query_id, 'search_email.log')

    async def _process_search(self, db):
        mentions_html, leaks_html, acc_search_html, fitness_tracker, acc_checker = '', '', '', '', ''
        filters = {"free_kwds": ""}
        mentions_html = {"all": ""}

        if 'mentions' in self.methods_type:
            try:
                mentions_html, filters = await self.xmlriver_email_do_request(db)
            except Exception as e:
                self.money_to_return += 5
                print(e)

        if 'acc checker' in self.methods_type:
            try:
                lampyre_email = lampyre_email_script.LampyreMail()
                acc_checker = lampyre_email.main(self.email, ['acc checker'])
            except Exception as e:
                self.money_to_return += 130
                print(e)

        html = response_email_template(
            self.email,
            mentions_html,
            filters,
            leaks_html,
            acc_search_html,
            fitness_tracker,
            acc_checker,
        )

        self.save_stats_to_file('search_email.log')
        file_storage = FileStorageService()
        await db_transactions.save_html(html, self.query_id, db, file_storage)

    async def _update_balances(self, db):
        await utils.renew_xml_balance(db)
        await utils.renew_lampyre_balance(db)

    async def xmlriver_email_do_request(self, db):
        all_found_data = []
        urls = []
        proh_sites = await read_needless_sites(db)
        max_attempts = 5
        retry_delay = 2

        # Обработка Google запроса
        url = SEARCH_ENGINES['google'] + f'"{self.email}"'
        
        for attempt in range(1, max_attempts + 1):
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(url=url)
                    handling_resp = handle_xmlriver_response(url, response, all_found_data, [], self.email)
                    
                    if handling_resp not in ('500', '110', '111'):
                        urls.append(url)
                        update_stats(self.request_stats, self.stats_lock, attempt, success=True)
                        break
                    else:
                        self.logger.log_error(f"{handling_resp} | URL: {url} | Попытка: {attempt}")
                        if attempt < max_attempts:
                            await asyncio.sleep(retry_delay)
            except Exception as e:
                self.logger.log_error(f"Исключение: {str(e)} | URL: {url} | Попытка: {attempt}")
                if attempt < max_attempts:
                    await asyncio.sleep(retry_delay)
        else:
            self.logger.log_error(f"Google запрос полностью провален: {url}")
            update_stats(self.request_stats, self.stats_lock, attempt, success=False)

        # Обработка Yandex запросов
        counter = 0
        while True:
            url = form_yandex_query_email(self.email, page_num=counter)
            
            for attempt in range(1, max_attempts + 1):
                try:
                    async with httpx.AsyncClient() as client:
                        response = await client.get(url=url)
                        handling_resp = handle_xmlriver_response(url, response, all_found_data, proh_sites, self.email)
                        
                        if handling_resp == '15':
                            update_stats(self.request_stats, self.stats_lock, attempt, success=True)
                            urls.append(url)
                            break
                        elif handling_resp in ('500', '110', '111'):
                            self.logger.log_error(f"{handling_resp} | URL: {url} | Попытка: {attempt}")
                            if attempt < max_attempts:
                                await asyncio.sleep(retry_delay)
                        else:
                            urls.append(url)
                            update_stats(self.request_stats, self.stats_lock, attempt, success=True)
                            counter += 1
                            break
                except Exception as e:
                    self.logger.log_error(f"Исключение: {str(e)} | URL: {url} | Попытка: {attempt}")
                    if attempt < max_attempts:
                        await asyncio.sleep(retry_delay)
            else:
                self.logger.log_error(f"Yandex запрос полностью провален: {url}")
                update_stats(self.request_stats, self.stats_lock, attempt, success=False)
            
            if handling_resp == '15':
                break

        items, filters = form_number_response_html(all_found_data, self.email)
        await write_urls(urls, "email")
        return items, filters

class CompanySearchTask(BaseSearchTask):
    def __init__(self, search_filters: Tuple):
        super().__init__(search_filters[7], search_filters[8])
        self.company_names = [search_filters[0], search_filters[1]]
        self.location = search_filters[2]
        self.keywords_from_user = search_filters[3]
        self.default_keywords_type = search_filters[4]
        self.plus_words = search_filters[5]
        self.minus_words = search_filters[6]
        self.search_engines = search_filters[9]
        self.languages = search_filters[10] if len(search_filters) > 10 else ['ru']
        self.logger = SearchLogger(self.query_id, 'search_company.log')

    async def _process_search(self, db):
        threads: List[Thread] = []
        all_found_info: List[FoundInfo] = []
        request_input_pack: List[tuple] = []
        urls = []
        titles = []

        try:
            prohibited_sites_list = await utils.add_sites_from_db([], db)
            keywords: dict = await get_default_keywords(db, self.default_keywords_type, self.languages)
            keywords_from_db = keywords[1]

            for lang in self.languages:
                len_keywords_from_user = len(self.keywords_from_user[lang]['keywords'])
                len_keywords_from_db = len(keywords_from_db[lang])
                for company_name in self.company_names:
                    if company_name == '':
                        break
                    if len_keywords_from_user == 0 and len_keywords_from_db == 0:
                        for engine in self.search_engines:
                            if url := SEARCH_ENGINES.get(engine):
                                form_input_pack_company(
                                    request_input_pack,
                                    company_name,
                                    "",
                                    "free word",
                                    self.location[lang],
                                    self.plus_words[lang],
                                    self.minus_words[lang],
                                    lang,
                                    url,
                                )
                    else:
                        for kwd_from_user in self.keywords_from_user[lang]['keywords']:
                            for engine in self.search_engines:
                                if url := SEARCH_ENGINES.get(engine):
                                    form_input_pack_company(
                                        request_input_pack,
                                        company_name,
                                        kwd_from_user,
                                        "free word",
                                        self.location[lang],
                                        self.plus_words[lang],
                                        self.minus_words[lang],
                                        lang,
                                        url,
                                    )

                        for words_type, words in keywords_from_db[lang].items():
                            for kwd_from_db in words:
                                for engine in self.search_engines:
                                    if url := SEARCH_ENGINES.get(engine):
                                        form_input_pack_company(
                                            request_input_pack,
                                            company_name,
                                            kwd_from_db,
                                            words_type,
                                            self.location[lang],
                                            self.plus_words[lang],
                                            self.minus_words[lang],
                                            lang,
                                            url,
                                        )

            for input_data in request_input_pack:
                url = input_data[0]
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
                            urls,
                            self.request_stats,
                            self.stats_lock,
                            self.logger,
                        ),
                    ),
                )

            manage_threads(threads)
            self.save_stats_to_file('search_company.log')
            company_titles = form_extra_titles(self.company_names[1], self.location['original'])
            titles.extend(
                form_titles(
                    self.company_names[0],
                    self.default_keywords_type,
                    self.keywords_from_user['original'],
                    self.minus_words['original'],
                    self.plus_words['original'],
                    'company',
                ),
            )

            languages_names = await get_languages_by_code(db, self.languages)
            titles.append(languages_names)

            items, filters, fullname_counters = form_response_html(all_found_info)

            html = response_company_template(
                titles,
                items,
                filters,
                fullname_counters,
                company_titles,
            )
            file_storage = FileStorageService()

            await db_transactions.save_html(html, self.query_id, db, file_storage)

        except Exception as e:
            print(e)
            self.money_to_return = self.price
            raise e

        await write_urls(urls, "company")

    async def _update_balances(self, db):
        await utils.renew_xml_balance(db)


class TelegramSearchTask(BaseSearchTask):
    def __init__(self, search_filters: Tuple):
        super().__init__(search_filters[2], 0)  # Цена не используется для Telegram поиска
        self.username = search_filters[0]
        self.tg_user_id = str(search_filters[1])
        self.methods_type = search_filters[4]

    async def _process_search(self, db):
        interests_html, groups1_html, groups2_html, profiles_html, phones_html = '', '', '', '', ''

        if 'interests' in self.methods_type:
            try:
                interests_html = get_interests(self.tg_user_id)
            except Exception as e:
                print(e)

        if 'groups_1' in self.methods_type:
            try:
                groups1_html = get_groups_ibhldr_method(self.tg_user_id)
            except Exception as e:
                print(e)

        if 'groups_2' in self.methods_type:
            try:
                groups2_html = get_groups_tgdev_method(self.tg_user_id)
            except Exception as e:
                print(e)

        if 'profile_history' in self.methods_type:
            try:
                profiles_html = get_profiles(self.tg_user_id)
            except Exception as e:
                print(e)

        if "phone_number" in self.methods_type:
            try:
                phones_html = get_phones(self.tg_user_id)
            except Exception as e:
                print(e)

        html = response_tg_template(
            self.username + "ID" + self.tg_user_id if self.username != "" else self.tg_user_id,
            interests_html,
            groups1_html,
            groups2_html,
            profiles_html,
            phones_html,
        )

        file_storage = FileStorageService()

        await db_transactions.save_html(html, self.query_id, db, file_storage)


@shared_task(bind=True, acks_late=True)
def start_search_by_num(self, phone_num, methods_type, query_id, price):
    loop = get_event_loop()
    task = NumberSearchTask(phone_num, methods_type, query_id, price)
    loop.run_until_complete(task.execute())


@shared_task(bind=True, acks_late=True)
def start_search_by_email(self, email, methods_type, query_id, price):
    loop = get_event_loop()
    task = EmailSearchTask(email, methods_type, query_id, price)
    loop.run_until_complete(task.execute())


@shared_task(bind=True, acks_late=True)
def start_search_by_company(self, search_filters):
    loop = get_event_loop()
    task = CompanySearchTask(search_filters)
    loop.run_until_complete(task.execute())


@shared_task(bind=True, acks_late=True)
def start_search_by_telegram(self, search_filters):
    loop = get_event_loop()
    task = TelegramSearchTask(search_filters)
    loop.run_until_complete(task.execute())


def lampyre_num_do_request(phone_num):
    lampyre_obj = Lampyre()
    lampyre_resp = lampyre_obj.main(phone_num)
    return lampyre_resp


def form_page_query(url, page_num):
    return f'{url}&page={page_num}'


def form_yandex_query_num(num: str, page_num):
    phone_num = num.replace("+", "%2B")
    url = SEARCH_ENGINES['yandex'] + f'{phone_num}&page={page_num}'
    return url


def form_google_query(phone_num: str):
    search_keys = []
    query_variants = format_phone_number(phone_num)
    for query in query_variants:
        search_key = SEARCH_ENGINES['google'] + f'''{query}'''
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
    url = SEARCH_ENGINES['yandex'] + f'"{email}"&page={page_num}'
    return url


async def read_needless_sites(db):
    result = await db.execute(
        select(ProhibitedPhoneSites.site_link)
    )
    return result.scalars().all()


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
    input_pack.append((url, keyword, keyword_type))


def form_extra_titles(second_name, location):
    extra_titles = ""
    if second_name != "":
        extra_titles += f'<span class="max-text-length" title="Дополнительное наименование: {second_name}"><b>Дополнительное наименование:</b> {second_name}</span>'

    if location != "":
        extra_titles += f'<span class="max-text-length" title="Местонахождение: {location}"><b>Местонахождение:</b> {location}</span>'

    return extra_titles


@shared_task
def delete_query_task(query_id):
    import logging
    logging.info(f"Celery: Попытка удалить query {query_id}")
    async def _delete():
        try:
            async with async_session() as db:
                # Удаление файлов, связанных с query_id
                file_storage = FileStorageService()
                result = await db.execute(select(TextData).where(TextData.query_id == query_id))
                text_data = result.scalars().first()
                if text_data and text_data.file_path:
                    try:
                        await file_storage.delete_query_data(text_data.file_path)
                        logging.info(f"Файл {text_data.file_path} успешно удалён.")
                    except Exception as e:
                        logging.error(f"Ошибка при удалении файла {text_data.file_path}: {e}")
                # Удаление самого запроса и связанных записей
                await delete_query_by_id(query_id, db)
        except Exception as e:
            logging.error(f"Celery: Ошибка при удалении query {query_id}: {e}")

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop = asyncio.get_event_loop()
    loop.run_until_complete(_delete())
