import logging
from typing import Tuple, List
from threading import Thread

from celery import shared_task

from server.api.dao.services_balance import ServicesBalanceDAO
from server.api.dao.text_data import TextDataDAO
from server.api.dao.language import LanguageDAO
from server.api.dao.keywords import KeywordsDAO
from server.api.dao.prohibited_sites import ProhibitedSitesDAO
from server.api.models.models import QueriesData
from server.api.templates.html_work import response_template
from server.api.services.file_storage import FileStorageService
from server.tasks.celery_config import (
    SEARCH_ENGINES,
    FoundInfo,
    get_event_loop,
)
from server.tasks.forms.forms import form_name_cases, form_search_key, form_titles
from server.tasks.forms.inputs import form_input_pack
from server.tasks.forms.responses import form_response_html
from server.tasks.logger import SearchLogger
from server.tasks.base.base import BaseSearchTask

from server.tasks.services import manage_threads, write_urls
from server.tasks.xmlriver import do_request_to_xmlriver


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
            prohibited_sites_list = await ProhibitedSitesDAO.add_sites_from_db([], db)
            keywords: dict = await KeywordsDAO.get_default_keywords(db, self.default_keywords_type, self.languages)
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

            languages_names = await LanguageDAO.get_languages_by_code(db, self.languages)
            titles.append(languages_names)

            manage_threads(threads)
            self.save_stats_to_file('search_name.log')
            await write_urls(urls, "name")

            items, filters, fullname_counters = form_response_html(all_found_info)
            html = response_template(titles, items, filters, fullname_counters)

            file_storage = FileStorageService()

            await TextDataDAO.save_html(html, self.query_id, db, file_storage)

        except Exception as e:
            print(e)
            self.money_to_return = self.price
            raise e

    async def _update_balances(self, db):
        await ServicesBalanceDAO.renew_xml_balance(db)

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
        # Создаем очередь для сбора результатов из потоков
        from queue import Queue
        results_queue = Queue()

        def worker(input_data, queue):
            try:
                url = input_data[0]
                keyword = input_data[1]
                keyword_type = input_data[2]
                name_case = input_data[3]

                raw_data = do_request_to_xmlriver(
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
                )
                queue.put(raw_data)
            except Exception as e:
                self.logger.log_error(f"Error in worker thread: {str(e)}")
                queue.put([])

        # Запускаем все потоки
        for input_data in request_input_pack:
            t = Thread(target=worker, args=(input_data, results_queue))
            threads.append(t)
            t.start()

        # Ждем завершения всех потоков
        for t in threads:
            t.join()

        # Собираем все результаты
        all_raw_data = []
        while not results_queue.empty():
            all_raw_data.extend(results_queue.get())

        # Сохраняем результаты
        await self.save_raw_results(all_raw_data, db)

    async def save_raw_results(self, raw_data, db):
        """Сохраняет результаты поиска в таблицу queries_data, каждый элемент как отдельную запись"""
        try:
            for item in raw_data:
                title = item.get('title', '')
                snippet = item.get('snippet', '')
                url = item.get('url')

                info = ""
                if title or snippet:
                    info = f"{title}: {snippet}" if title and snippet else f"{title}{snippet}"

                query_data = QueriesData(
                    query_id=self.query_id,
                    found_info=info if info else "No information found",
                    found_links=[url] if url else [],
                )

                db.add(query_data)
                logging.info(f"Processing item - Title: {title}, URL: {url}")
            await db.commit()
            logging.info(f"Raw data saved for query {self.query_id} - {len(raw_data)} records")

        except Exception as e:
            logging.error(f"Failed to save raw results: {e}")
            await db.rollback()
            raise


@shared_task(bind=True, acks_late=True, queue='name_tasks')
def start_search_by_name(self, search_filters):
    loop = get_event_loop()
    task = NameSearchTask(search_filters)
    loop.run_until_complete(task.execute())
