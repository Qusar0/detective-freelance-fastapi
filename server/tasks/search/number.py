import logging
import time
from typing import List

from celery import shared_task
import requests

from server.api.scripts import utils, db_transactions
from server.api.scripts.get_contact_script import get_tags_in_getcontact
from server.api.scripts.html_work import response_num_template
from server.api.services.file_storage import FileStorageService
from server.tasks.celery_config import (
    get_event_loop,
)
from server.tasks.forms.responses import form_number_response_html
from server.tasks.forms.sites import form_google_query, form_yandex_query_num
from server.tasks.logger import SearchLogger
from server.tasks.base.base import BaseSearchTask

from server.tasks.services import read_needless_sites, update_stats, write_urls
from server.tasks.xmlriver import handle_xmlriver_response


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

        if 'mentions' in self.methods_type:
            try:
                items, filters = await self.xmlriver_num_do_request(db)
            except Exception as e:
                self.money_to_return += 5
                print(e)

        if 'tags' in self.methods_type:
            try:
                tags, self.requests_getcontact_left = get_tags_in_getcontact(self.phone_num)
            except Exception as e:
                self.money_to_return += 25
                print(e)

        html = response_num_template(
            self.phone_num,
            items,
            filters,
            lampyre_html,
            tags,
            acc_search_html,
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


@shared_task(bind=True, acks_late=True)
def start_search_by_num(self, phone_num, methods_type, query_id, price):
    loop = get_event_loop()
    task = NumberSearchTask(phone_num, methods_type, query_id, price)
    loop.run_until_complete(task.execute())
