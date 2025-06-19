import requests
import logging
from server.api.conf.config import settings

# contact
def get_tags_in_getcontact(number):
    headers = {
        'x-bot-id': str(settings.telegram_api_id),
        'x-bot-token': str(settings.telegram_api_hash),
        'x-api-key': str(settings.telegram_db_encryption_key),
        'Content-Type': 'application/json',
    }

    try:
        r = requests.post(
            'https://r0cyk3wpdg.execute-api.us-east-2.amazonaws.com/default/apiv2',
            headers=headers,
            json={"phone": str(number)}
        )
        r.raise_for_status
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return [], 0

    contacs_json = r.json()
    requests_left = contacs_json['data']['subscription']['remainingRequestCount']
    sources = contacs_json['data']['responce']

    list_tags = []
    for source in sources:
        if source['source'] == 'getcontact':
            response = source['results']['response']
            if 'tagCount' in response and response['tagCount'] > 0:
                extra = response.get('extra', [])
                if extra:
                    tags = extra['tags']
                    list_tags.extend([tag['tag'] for tag in tags if 'tag' in tag])
            else:
                logging.info(f"Для номера {number} теги не найдены.")
    return list_tags, requests_left
