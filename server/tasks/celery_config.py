import asyncio
from server.api.conf.config import settings


SEARCH_ENGINES = {
    'google': (
        f'http://xmlriver.com/search/xml'
        f'?user={settings.xml_river_user_id}'
        f'&key={settings.xml_river_api_key}'
        f'&query='
    ),
    'yandex': (
        f'http://xmlriver.com/search_yandex/xml'
        f'?user={settings.xml_river_user_id}'
        f'&key={settings.xml_river_api_key}'
        f'&groupby=10'
        f'&query='
    ),
}


def get_event_loop():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop
