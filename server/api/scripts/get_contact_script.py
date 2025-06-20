import requests
import logging
from server.api.conf.config import settings


def _handle_callapp(response):
    """Обрабатывает ответ от сервиса CallApp."""
    data = {}
    if 'name' in response:
        data['name'] = response['name']
    if 'addresses' in response:
        data['addresses'] = [addr['street'] for addr in response['addresses']]
    if 'categories' in response:
        data['categories'] = [cat['name'] for cat in response['categories']]
    if 'websites' in response:
        data['websites'] = [site['websiteUrl'] for site in response['websites']]
    if 'facebookID' in response:
        data['facebook_id'] = response['facebookID']['id']
    return data


def _handle_whatsapp(response):
    """Обрабатывает ответ от сервиса WhatsApp."""
    data = {}
    if 'businessProfile' in response:
        profile = response['businessProfile']
        data['business_address'] = profile.get('address', '')
        data['business_category'] = profile.get('category', '')
        data['business_description'] = profile.get('description', '')
        data['business_email'] = profile.get('email', '')
        if 'website' in profile:
            data['business_websites'] = [site['url'] for site in profile['website']]
    if 'status' in response:
        data['whatsapp_status'] = response['status']
    return data


def _handle_callerid(response):
    """Обрабатывает ответ от сервиса CallerID."""
    data = {}
    if 'name' in response:
        data['caller_name'] = response['name']
    return data


def _handle_eyecon(response):
    """Обрабатывает ответ от сервиса Eyecon."""
    data = {}
    if 'contacts' in response:
        data['contacts'] = [contact['name'] for contact in response['contacts']]
    return data


def parse_getcontact_response(response_data):
    """
    Парсит данные из JSON-ответа GetContact API, пропуская 404 ошибки.
    Делегирует обработку каждого источника отдельной функции.
    """
    if response_data.get('apiStatusCode') != 200:
        return {}

    phone_data = {
        'phone': response_data['data']['request'],
        'sources': {}
    }

    handler_map = {
        'callapp': _handle_callapp,
        'whatsapp': _handle_whatsapp,
        'callerid': _handle_callerid,
        'eyecon': _handle_eyecon,
    }

    for source in response_data['data']['responce']:
        if source['results']['statusCode'] == 404:
            continue

        source_name = source['source']
        response = source['results']['response']

        if handler := handler_map.get(source_name):
            phone_data['sources'].update(handler(response))

    return phone_data

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
        r.raise_for_status()

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
                    print(f"Для номера {number} теги не найдены.")
        
        parsed_data = parse_getcontact_response(contacs_json)
        return list_tags, requests_left, parsed_data
        
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return [], 0, {}
