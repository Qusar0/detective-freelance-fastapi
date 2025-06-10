import asyncio
from recordtype import recordtype

from server.api.conf.config import settings

SEARCH_ENGINES = {
    'google': f'http://xmlriver.com/search/xml?user={settings.xml_river_user_id}&key={settings.xml_river_api_key}&query=',
    'yandex': f'http://xmlriver.com/search_yandex/xml?user={settings.xml_river_user_id}&key={settings.xml_river_api_key}&groupby=10&query=',
}

FoundInfo = recordtype("FoundInfo", "title snippet url uri weight kwd word_type kwds_list fullname soc_type doc_type")
NumberInfo = recordtype("NumberInfo", "title snippet url uri weight kwd")


def get_event_loop():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop