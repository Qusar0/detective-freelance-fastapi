import asyncio
from typing import List
from celery import shared_task
import httpx

from server.api.scripts.lampyre_email import LampyreMail
from server.api.dao.services_balance import ServicesBalanceDAO
from server.api.dao.text_data import TextDataDAO
from server.api.dao.keywords import KeywordsDAO
from server.api.models.models import QueriesData, QueryDataKeywords
from server.api.templates.html_work import response_email_template
from server.api.services.file_storage import FileStorageService
from server.tasks.celery_config import (
    SEARCH_ENGINES,
    get_event_loop,
)
from server.tasks.forms.responses import form_number_response_html
from server.tasks.forms.sites import form_yandex_query_email
from server.tasks.logger import SearchLogger
from server.tasks.base.base import BaseSearchTask
from server.tasks.services import read_needless_sites, update_stats, write_urls
from server.tasks.xmlriver import handle_xmlriver_response


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
                result = await self.xmlriver_email_do_request(db)
                await self.save_raw_results(result['raw_data'], db)
                mentions_html, filters = result['processed_data']
            except Exception as e:
                self.money_to_return += 5
                self.logger.log_error(f"Ошибка в получении упоминаний: {e}")

        if 'acc checker' in self.methods_type:
            try:
                lampyre_email = LampyreMail()
                acc_checker = lampyre_email.main(self.email, ['acc checker'])
            except Exception as e:
                self.money_to_return += 130
                self.logger.log_error(f"Ошибка в проверке аккаунтов: {e}")

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
        await TextDataDAO.save_html(html, self.query_id, db, file_storage)

    async def _update_balances(self, db):
        await ServicesBalanceDAO.renew_xml_balance(db)
        await ServicesBalanceDAO.renew_lampyre_balance(db)

    async def save_raw_results(self, raw_data, db):
        """Сохраняет сырые результаты поиска в базу данных"""
        try:
            for url, item in raw_data.items():
                title = item.get('raw_title') or item.get('title')
                snippet = item.get('raw_snippet') or item.get('snippet')
                publication_date = item.get('pubDate')
                keyword_type = 'free word'

                query_data = QueriesData(
                    query_id=self.query_id,
                    title=title,
                    info=snippet,
                    link=url,
                    publication_date=publication_date,
                )
                db.add(query_data)
                await db.flush()

                original_keyword_id = await KeywordsDAO.get_keyword_id(db, 'free word', keyword_type)
                query_data_keyword = QueryDataKeywords(
                    query_data_id=query_data.id,
                    keyword='ключевых слов нет',
                    original_keyword_id=original_keyword_id,
                )
                db.add(query_data_keyword)
            await db.commit()
        except Exception as e:
            await db.rollback()
            self.logger.log_error(f"Failed to save raw results: {e}")
            raise

    async def xmlriver_email_do_request(self, db):
        all_raw_data = {}
        all_found_data = []
        urls = []
        proh_sites = await read_needless_sites(db)
        max_attempts = 5
        retry_delay = 2

        url = SEARCH_ENGINES['google'] + f'"{self.email}"'
        existing_urls = set()
        for attempt in range(1, max_attempts + 1):
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(url=url)
                    handling_resp = handle_xmlriver_response(
                        response,
                        all_found_data,
                        [],
                        self.email,
                        all_raw_data,
                        existing_urls,
                    )

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

        counter = 0
        while True:
            url = form_yandex_query_email(self.email, page_num=counter)

            for attempt in range(1, max_attempts + 1):
                try:
                    async with httpx.AsyncClient() as client:
                        response = await client.get(url=url)
                        handling_resp = handle_xmlriver_response(
                            response,
                            all_found_data,
                            proh_sites,
                            self.email,
                            all_raw_data,
                            existing_urls,
                        )

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

        await write_urls(urls, "email")
        return {
            'raw_data': all_raw_data,
            'processed_data': form_number_response_html(all_found_data, self.email)
        }


@shared_task(bind=True, acks_late=True, queue='email_tasks')
def start_search_by_email(self, email, methods_type, query_id, price):
    loop = get_event_loop()
    task = EmailSearchTask(email, methods_type, query_id, price)
    loop.run_until_complete(task.execute())
