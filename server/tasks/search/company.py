from typing import Tuple, List
from threading import Thread

from celery import shared_task

from server.api.dao.prohibited_sites import ProhibitedSitesDAO
from server.api.dao.keywords import KeywordsDAO
from server.api.dao.language import LanguageDAO
from server.api.dao.services_balance import ServicesBalanceDAO
from server.api.dao.text_data import TextDataDAO
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

from server.tasks.services import manage_threads, write_urls
from server.tasks.xmlriver import do_request_to_xmlriver


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
            prohibited_sites_list = await ProhibitedSitesDAO.add_sites_from_db([], db)
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

        except Exception as e:
            print(e)
            self.money_to_return = self.price
            raise e

        await write_urls(urls, "company")

    async def _update_balances(self, db):
        await ServicesBalanceDAO.renew_xml_balance(db)


@shared_task(bind=True, acks_late=True)
def start_search_by_company(self, search_filters):
    loop = get_event_loop()
    task = CompanySearchTask(search_filters)
    loop.run_until_complete(task.execute())
