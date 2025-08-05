from typing import Tuple, List
import threading
from queue import Queue
import logging

from celery import shared_task

from server.api.dao.prohibited_sites import ProhibitedSitesDAO
from server.api.dao.keywords import KeywordsDAO
from server.api.dao.language import LanguageDAO
from server.api.dao.services_balance import ServicesBalanceDAO
from server.api.dao.text_data import TextDataDAO
from server.api.models.models import QueriesData
from server.api.templates.html_work import response_company_template
from server.api.services.file_storage import FileStorageService
from server.tasks.celery_config import (
    SEARCH_ENGINES,
    FoundInfo,
    get_event_loop,
)
from server.tasks.forms.forms import form_extra_titles, form_titles
from server.tasks.forms.inputs import form_input_pack_company
from server.tasks.forms.responses import form_response_html
from server.tasks.logger import SearchLogger
from server.tasks.base.base import BaseSearchTask

from server.tasks.services import write_urls, manage_threads
from server.tasks.xmlriver import search_worker


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
        all_found_info: List[FoundInfo] = []
        request_input_pack: List[tuple] = []
        urls = []
        titles = []

        try:
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
                    self.minus_words['original'],
                    self.plus_words['original'],
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
            print(e)
            self.money_to_return = self.price
            raise e

    async def _process_search_requests(
        self,
        request_input_pack,
        all_found_info,
        urls,
        db,
    ):
        shared_results = []
        thread_list = []

        for input_data in request_input_pack:
            t = threading.Thread(
                target=search_worker,
                args=(
                    input_data,
                    shared_results,
                    all_found_info,
                    urls,
                    self.request_stats,
                    self.stats_lock,
                    self.logger
                )
            )
            thread_list.append(t)

        manage_threads(thread_list)
        await self.save_raw_results(shared_results, db)

    async def save_raw_results(self, raw_data, db):
        """Сохраняет результаты поиска в таблицу queries_data, каждый элемент как отдельную запись"""
        try:
            logging.info(f"Raw data to save: {raw_data}")

            for item in raw_data:
                title = item.get('title')
                snippet = item.get('snippet')
                url = item.get('url')
                publication_date = item.get('publication_date')

                query_data = QueriesData(
                    query_id=self.query_id,
                    title=title,
                    info=snippet,
                    link=url,
                    publication_date=publication_date,
                )

                db.add(query_data)
                logging.info(f"Processing item - Title: {title}, URL: {url}")
            await db.commit()
            logging.info(f"Raw data saved for query {self.query_id} - {len(raw_data)} records")

        except Exception as e:
            logging.error(f"Failed to save raw results: {e}")
            await db.rollback()
            raise

    async def _update_balances(self, db):
        await ServicesBalanceDAO.renew_xml_balance(db)


@shared_task(bind=True, acks_late=True, queue='company_tasks')
def start_search_by_company(self, search_filters):
    loop = get_event_loop()
    task = CompanySearchTask(search_filters)
    loop.run_until_complete(task.execute())
