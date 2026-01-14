from typing import Tuple, List
import asyncio
import datetime
from loguru import logger
from celery import shared_task

from server.api.dao.language import LanguageDAO
from server.api.dao.services_balance import ServicesBalanceDAO
from server.api.dao.text_data import TextDataDAO
from server.api.dao.query_search_category import QuerySearchCategoryDAO
from server.api.dao.additional_query_word import AdditionalQueryWordDAO
from server.api.dao.prohibited_sites import ProhibitedSitesDAO
from server.api.dao.queries_data import QueriesDataDAO
from server.api.dao.keywords import KeywordsDAO
from server.api.templates.html_work import response_company_template
from server.api.services.file_storage import FileStorageService
from server.tasks.celery_config import SEARCH_ENGINES, get_event_loop
from server.api.schemas.query import FoundInfo
from server.tasks.services import get_http_client
from server.tasks.forms.forms import form_extra_titles, form_titles
from server.tasks.forms.inputs import form_input_pack_company
from server.tasks.forms.responses import form_response_html
from server.logger import SearchLogger
from server.tasks.base.base import BaseSearchTask
from server.tasks.services import manage_async_tasks, write_urls
from server.tasks.xmlriver import search_worker


class CompanySearchTask(BaseSearchTask):
    def __init__(self, search_filters: Tuple):
        super().__init__(search_filters[7], search_filters[8])
        self.company_names = [search_filters[0], search_filters[1]]
        self.location = search_filters[2]
        self.keywords_from_user = search_filters[3]
        self.default_keywords_type = search_filters[4]
        self.search_plus = search_filters[5]
        self.search_minus = search_filters[6]
        self.search_engines = search_filters[9]
        self.languages = search_filters[10] if len(search_filters) > 10 else ['ru']
        self.logger = SearchLogger(self.query_id, 'search_company.log')

    async def _process_search(self, db):
        all_found_info: List[FoundInfo] = []
        request_input_pack: List[tuple] = []
        urls = []
        titles = []

        try:
            await self._save_general_info(db)

            keywords: dict = await KeywordsDAO.get_default_keywords(db, self.default_keywords_type, self.languages)
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
                                    "free word",
                                    self.location[lang],
                                    self.search_plus[lang],
                                    self.search_minus[lang],
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
                                        "free word",
                                        self.location[lang],
                                        self.search_plus[lang],
                                        self.search_minus[lang],
                                        lang,
                                        url,
                                    )

                        for words_type, words in keywords_from_db[lang].items():
                            original_words = keywords_from_db['original'][words_type]
                            for kwd_from_db, original_kwd_from_db in zip(words, original_words):
                                for engine in self.search_engines:
                                    if url := SEARCH_ENGINES.get(engine):
                                        form_input_pack_company(
                                            request_input_pack,
                                            company_name,
                                            kwd_from_db,
                                            original_kwd_from_db,
                                            words_type,
                                            self.location[lang],
                                            self.search_plus[lang],
                                            self.search_minus[lang],
                                            lang,
                                            url,
                                        )

            await self._process_search_requests(
                request_input_pack,
                all_found_info,
                urls,
                db,
            )

            self.save_stats_to_file('search_company.log')
            company_titles = form_extra_titles(self.company_names[1], self.location['original'])
            titles.extend(
                form_titles(
                    self.company_names[0],
                    self.default_keywords_type,
                    self.keywords_from_user['original'],
                    self.search_minus['original'],
                    self.search_plus['original'],
                    'company',
                ),
            )

            languages_names = await LanguageDAO.get_languages_by_code(db, self.languages)
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

            await TextDataDAO.save_html(html, self.query_id, db, file_storage)
            await write_urls(urls, "company")

        except Exception as e:
            logger.error(f"Возникла ошибка в поиске по компании: {str(e)}")
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

    async def save_raw_results(self, raw_data, db):
        """Сохраняет результаты поиска в таблицу queries_data через DAO"""
        await QueriesDataDAO.bulk_save_query_results(self.query_id, raw_data, db)

    async def _update_balances(self, db):
        await ServicesBalanceDAO.renew_xml_balance(db)


@shared_task(bind=True, acks_late=True, queue='company_tasks')
def start_search_by_company(self, search_filters):
    loop = get_event_loop()
    task = CompanySearchTask(search_filters)
    loop.run_until_complete(task.execute())
