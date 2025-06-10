import logging
import xmltodict
import os
import re
import time
from typing import List
from urllib.parse import urlparse
import requests

from server.api.error.errors import CustomError
from server.tasks.celery_config import SEARCH_ENGINES, FoundInfo, NumberInfo
from server.tasks.forms.sites import form_page_query
from server.tasks.logger import SearchLogger
from server.tasks.services import update_stats


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