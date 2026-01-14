from loguru import logger
import xmltodict
import os
import re
import asyncio
from typing import List, Union, Optional, Dict, Any, Set
from urllib.parse import urlparse
import httpx

from server.tasks.celery_config import SEARCH_ENGINES
from server.tasks.forms.sites import form_page_query
from server.logger import SearchLogger
from server.tasks.services import update_stats_async
from server.api.schemas.query import FoundInfo, NumberInfo


async def do_request_to_xmlriver(
    input_data,
    all_found_data,
    prohibited_sites,
    urls,
    request_stats,
    stats_lock,
    search_logger: SearchLogger,
    existing_urls,
    results_container,
    client: httpx.AsyncClient,
):
    url, keyword, original_keyword, keyword_type, name_case = input_data
    max_attempts = 5
    base_retry_delay = 0.5

    async def process_request(target_url, existing_urls: Set[str]):
        for attempt in range(1, max_attempts + 1):
            try:
                response = await client.get(target_url, timeout=30.0)

                handling_resp = await handle_xmlriver_response(
                    response,
                    all_found_data,
                    prohibited_sites,
                    keyword,
                    results_container,
                    existing_urls,
                    name_case,
                    keyword_type,
                    original_keyword,
                    stats_lock,
                )

                if handling_resp == '15':
                    return False

                if handling_resp not in ('500', '110', '111'):
                    urls.append(target_url)
                    await update_stats_async(request_stats, stats_lock, attempt, success=True)
                    return True

                search_logger.log_error(f"{handling_resp} | URL: {target_url} | Попытка: {attempt}")

            except Exception as e:
                search_logger.log_error(f"Исключение: {str(e)} | URL: {target_url} | Попытка: {attempt}")

            if attempt < max_attempts:
                await asyncio.sleep(base_retry_delay)

        await update_stats_async(request_stats, stats_lock, max_attempts, success=False)
        search_logger.log_error(f"Запрос полностью провален: {target_url}")
        return False

    if SEARCH_ENGINES['google'] in url:
        logger.info(f"Обработка Google запроса: {url}")
        await process_request(url, existing_urls)

    elif SEARCH_ENGINES['yandex'] in url:
        logger.info(f"Обработка Yandex запроса: {url}")
        page_num = 0
        success = True
        while success:
            new_url = form_page_query(url, page_num)
            success = await process_request(new_url, existing_urls)
            page_num += 1


async def handle_xmlriver_response(  # noqa: WPS211
    response: httpx.Response,
    all_found_data: List[Union[FoundInfo, NumberInfo]],
    prohibited_sites: List[str],
    keyword: str,
    raw_data: Dict[str, Dict[str, Any]],
    existing_urls: Set[str],
    name_case: Optional[List[str]] = None,
    keyword_type: Optional[str] = None,
    original_keyword: Optional[str] = None,
    stats_lock: Optional[asyncio.Lock] = None,
) -> Union[str, None]:
    """Обрабатывает ответ от XMLriver API."""
    SOCIAL_URLS = {
        'vk.com': 'Вконтакте',
        'ok.ru': 'Одноклассники',
        'www.facebook.com': 'Facebook',
        'www.instagram.com': 'Instagram',
        't.me': 'Telegram',
    }
    DOCUMENT_TYPES = {
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

    try:  # noqa: WPS229
        json_data = xmltodict.parse(response.content)
        response_data = json_data["yandexsearch"]["response"]

        if "error" in response_data:
            error_code = xml_errors_handler(json_data)
            logger.warning(f"Обнаружена ошибка в ответе: {error_code}")
            return error_code

        if response_data.get('fixtype') == 'quotes':
            return '15'

        groups = response_data["results"]["grouping"]["group"]
        groups = [groups] if isinstance(groups, dict) else groups

    except (KeyError, xmltodict.ParsingInterrupted) as e:
        logger.error(f"Некорректный ответ от XMLriver: {str(e)}")
        raise ValueError(f"Некорректный ответ от XMLriver: {str(e)}")

    for group in groups:
        doc = group["doc"]
        url = doc["url"]

        if stats_lock:
            async with stats_lock:
                if url in existing_urls:
                    raw_data[url]['weight'] += 1
                    raw_data[url]['keywords'].add((keyword, original_keyword, keyword_type))
                    continue
        else:
            if url in existing_urls:
                raw_data[url]['weight'] += 1
                raw_data[url]['keywords'].add((keyword, original_keyword, keyword_type))
                continue

        title = doc.get("title", '')
        passage_value = doc.get("passages", {}).get("passage")
        snippet = doc.get("fullsnippet") or ("" if passage_value is None else passage_value)
        processed_snippet = ''
        pub_date = doc.get("pubDate")

        parsed_url = urlparse(url)
        site_url = parsed_url.netloc
        file_ext = os.path.splitext(parsed_url.path)[1].lower()

        resource_type = SOCIAL_URLS.get(site_url) or DOCUMENT_TYPES.get(file_ext) or None

        # Проверяем на запрещенные сайты
        if any(site.lower() in site_url.lower() for site in prohibited_sites):
            continue

        if snippet:
            processed_snippet = snippet.replace("`", "'").replace('\\', r'\\')
        if name_case is not None:
            processed_snippet = color_keywords(name_case, processed_snippet, keyword)

        has_patronymic = name_case and len(name_case) > 2
        patronymic_in_snippet = has_patronymic and name_case[2].lower() in snippet.lower()
        fullname_type = 'true' if patronymic_in_snippet else 'false'

        try:
            if name_case is None:
                if keyword_type:
                    found_info = FoundInfo(
                        title=title.replace("`", "'"),
                        snippet=processed_snippet,
                        url=site_url,
                        publication_date=pub_date,
                        uri=url,
                        weight=1,
                        kwd=keyword,
                        word_type=keyword_type,
                        kwds_list=[keyword],
                        fullname='true',
                        soc_type=resource_type,
                        doc_type='',
                    )
                else:
                    found_info = NumberInfo(
                        title=title.replace("`", "'"),
                        snippet=processed_snippet,
                        url=site_url,
                        uri=url,
                        weight=1,
                        kwd=keyword,
                    )
            else:
                found_info = FoundInfo(
                    title=title.replace("`", "'"),
                    snippet=processed_snippet,
                    url=site_url,
                    publication_date=pub_date,
                    uri=url,
                    weight=1,
                    kwd=keyword,
                    word_type=keyword_type,
                    kwds_list=[keyword],
                    fullname=fullname_type,
                    soc_type=resource_type,
                    doc_type='',
                )

            is_fullname = fullname_type == 'true' if name_case else False

            if stats_lock:
                async with stats_lock:
                    if url not in existing_urls:
                        raw_data[url] = {
                            'title': title,
                            'snippet': snippet,
                            'domain': site_url,
                            'pubDate': pub_date,
                            'keywords': {(keyword, original_keyword, keyword_type)},
                            'resource_type': resource_type,
                            'weight': 1,
                            'is_fullname': is_fullname
                        }
                        existing_urls.add(url)
                        all_found_data.append(found_info)
                    else:
                        raw_data[url]['weight'] += 1
                        raw_data[url]['keywords'].add((keyword, original_keyword, keyword_type))
            else:
                if url not in existing_urls:
                    raw_data[url] = {
                        'title': title,
                        'snippet': snippet,
                        'domain': site_url,
                        'pubDate': pub_date,
                        'keywords': {(keyword, original_keyword, keyword_type)},
                        'resource_type': resource_type,
                        'weight': 1,
                        'is_fullname': is_fullname
                    }
                    existing_urls.add(url)
                    all_found_data.append(found_info)
                else:
                    raw_data[url]['weight'] += 1
                    raw_data[url]['keywords'].add((keyword, original_keyword, keyword_type))

        except Exception as e:
            logger.error(f"Ошибка при создании записи: {title}, {snippet}: {str(e)}")


def xml_errors_handler(xml_response):
    """Обрабатывает ошибку XMLRiver."""
    try:
        error_data = xml_response["yandexsearch"]["response"]["error"]
        error_code = error_data["@code"]
        error_text = error_data["#text"]
    except KeyError:
        raise ("XMLriver на обновлении.")

    if error_code == '101' and error_text == 'Сервис сбора данных на обновлении. Попробуйте чуть позже.':
        raise ("XMLriver на обновлении.")

    return error_code


def color_keywords(name_case: List[str], snippet: str, search_keyword: str) -> str:
    """Подсвечивает ключевые слова в тексте HTML-тегами."""
    if snippet is None:
        return ''

    name = name_case[0]
    surname = name_case[1]

    if len(name_case) == 2:
        patronymic = ""
    else:
        patronymic = name_case[2]

    keywords_list = [name, surname, patronymic, search_keyword]

    words = snippet.split()

    for word in words:
        for kw in keywords_list:
            if word.lower().strip(".,!?") == kw.lower():
                word = f'<span class="key-word">{word}</span>'

    marked_snippet = " ".join(words)
    colored_snippet = re.sub(
        search_keyword,
        f'<span class="key-word">{search_keyword}</span>',
        marked_snippet,
        flags=re.IGNORECASE,
    )

    return colored_snippet


async def search_worker(  # noqa: WPS211
    input_data,
    results_container: Dict[str, Dict[str, Any]],
    all_found_info,
    urls,
    request_stats,
    stats_lock,
    search_logger: SearchLogger,
    existing_urls,
    prohibited_sites,
    client: httpx.AsyncClient,
):
    """Асинхронная функция для выполнения поисковых запросов."""
    try:
        await do_request_to_xmlriver(
            input_data,
            all_found_info,
            prohibited_sites,
            urls,
            request_stats,
            stats_lock,
            search_logger,
            existing_urls,
            results_container,
            client,
        )
    except Exception as e:
        logger.error(f"Ошибка в рабочем потоке: {str(e)}")
