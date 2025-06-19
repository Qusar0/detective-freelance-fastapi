import asyncio
from typing import List

from celery import shared_task
import httpx

from server.api.scripts import lampyre_email_script, utils, db_transactions
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


@shared_task(bind=True, acks_late=True)
def start_search_by_email(self, email, methods_type, query_id, price):
    loop = get_event_loop()
    task = EmailSearchTask(email, methods_type, query_id, price)
    loop.run_until_complete(task.execute())
