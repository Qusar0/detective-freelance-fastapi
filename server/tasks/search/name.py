from loguru import logger
from typing import Tuple, List
import asyncio
import datetime

from celery import shared_task

from server.api.dao.services_balance import ServicesBalanceDAO
from server.api.dao.text_data import TextDataDAO
from server.api.dao.language import LanguageDAO
from server.api.dao.keywords import KeywordsDAO
from server.api.dao.additional_query_word import AdditionalQueryWordDAO
from server.api.dao.prohibited_sites import ProhibitedSitesDAO
from server.api.dao.query_search_category import QuerySearchCategoryDAO
from server.api.dao.queries_data import QueriesDataDAO
from server.api.templates.html_work import response_template
from server.api.services.file_storage import FileStorageService
from server.tasks.celery_config import SEARCH_ENGINES, get_event_loop
from server.api.schemas.query import FoundInfo
from server.tasks.services import get_http_client
from server.tasks.forms.forms import form_name_cases, form_search_key, form_titles
from server.tasks.forms.inputs import form_input_pack
from server.tasks.forms.responses import form_response_html
from server.logger import SearchLogger
from server.tasks.base.base import BaseSearchTask
from server.tasks.services import manage_async_tasks, write_urls
from server.tasks.xmlriver import search_worker


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
        all_found_info: List[FoundInfo] = []
        request_input_pack: List[tuple] = []
        urls = []

        try:
            await self._save_general_info(db)

            keywords = await KeywordsDAO.get_default_keywords(db, self.default_keywords_type, self.languages)
            keywords_from_db = keywords[1]
            titles = []

            original_full_name = [self.search_name['original'], self.search_surname['original']]
            if self.search_patronymic['original']:
                original_full_name.append(self.search_patronymic['original'])

            for lang in self.languages:
                full_name = [self.search_name[lang], self.search_surname[lang]]
                if self.search_patronymic[lang]:
                    full_name.append(self.search_patronymic[lang])

                name_cases = await form_name_cases(full_name, lang)

                await self._form_search_requests(
                    name_cases,
                    keywords_from_db,
                    request_input_pack,
                    lang,
                )

            await self._process_search_requests(
                request_input_pack,
                all_found_info,
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

            languages_names = await LanguageDAO.get_languages_by_code(db, self.languages)
            titles.append(languages_names)

            self.save_stats_to_file('search_name.log')
            await write_urls(urls, "name")

            items, filters, fullname_counters = form_response_html(all_found_info)
            html = response_template(titles, items, filters, fullname_counters)

            file_storage = FileStorageService()

            await TextDataDAO.save_html(html, self.query_id, db, file_storage)

        except Exception as e:
            logger.error(f"Возникла ошибка в поиске по имени: {str(e)}")
            self.money_to_return = self.price
            raise e

    async def _save_general_info(self, db):
        if self.default_keywords_type:
            await QuerySearchCategoryDAO.add_search_categories(
                db,
                self.query_id,
                self.default_keywords_type,
            )

        if self.search_minus['original']:
            await AdditionalQueryWordDAO.add_words(
                db,
                self.query_id,
                self.search_minus['original'],
                'minus',
            )
        if self.search_plus['original']:
            await AdditionalQueryWordDAO.add_words(
                db,
                self.query_id,
                self.search_plus['original'],
                'plus',
            )
        if self.keywords_from_user['original']:
            await AdditionalQueryWordDAO.add_words(
                db,
                self.query_id,
                self.keywords_from_user['original'],
                'free word',
            )

        if self.languages:
            await LanguageDAO.save_query_languages(db, self.query_id, self.languages)

    async def _update_balances(self, db):
        await ServicesBalanceDAO.renew_xml_balance(db)

    async def _form_search_requests(
        self,
        name_cases,
        keywords_from_db,
        request_input_pack,
        lang,
    ):
        len_keywords_from_user = len(self.keywords_from_user[lang]['keywords'])
        for name_case in name_cases:
            search_keys = form_search_key(name_case, len_keywords_from_user)
            for search_key in search_keys:
                if len_keywords_from_user == 0 and len(keywords_from_db[lang]) == 0:
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
            for words_type, words in keywords_from_db[lang].items():
                original_words = keywords_from_db['original'][words_type]
                for kwd_from_db, original_kwd_from_db in zip(words, original_words):
                    for engine in self.search_engines:
                        if url := SEARCH_ENGINES.get(engine):
                            form_input_pack(
                                request_input_pack,
                                search_key,
                                kwd_from_db,
                                original_kwd_from_db,
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
        all_found_info,
        urls,
        db,
    ):
        shared_results = {}
        existing_urls = set()
        prohibited_sites = await ProhibitedSitesDAO.select_general_needless_sites(db)

        async_stats_lock = asyncio.Lock()

        start_time = datetime.datetime.now()
        self.logger.log_error(f'Начало выполнения {start_time}')

        async with get_http_client() as client:
            tasks = [
                search_worker(
                    input_data,
                    shared_results,
                    all_found_info,
                    urls,
                    self.request_stats,
                    async_stats_lock,
                    self.logger,
                    existing_urls,
                    prohibited_sites,
                    client,
                )
                for input_data in request_input_pack
            ]
            await manage_async_tasks(tasks, max_concurrent=20)

        end_time = datetime.datetime.now()
        self.logger.log_error(f'Конец выполнения запросов {end_time}')
        self.logger.log_error(f'Время выполнения запросов {end_time - start_time}')
        await self.save_raw_results(shared_results, db)
        end_time = datetime.datetime.now()
        self.logger.log_error(f'Конец выполнения сохранения {end_time}')
        self.logger.log_error(f'Время выполнения сохранения {end_time - start_time}')

    async def save_raw_results(self, raw_data, db):
        """Сохраняет результаты поиска в таблицу queries_data через DAO"""
        await QueriesDataDAO.bulk_save_query_results(self.query_id, raw_data, db)


@shared_task(bind=True, acks_late=True, queue='name_tasks')
def start_search_by_name(self, search_filters):
    loop = get_event_loop()
    task = NameSearchTask(search_filters)
    loop.run_until_complete(task.execute())
