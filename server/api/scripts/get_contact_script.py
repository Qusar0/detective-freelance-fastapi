import requests
import logging
from server.api.conf.config import settings


def parse_getcontact_response(response_data):
    """
    Парсит данные из JSON-ответа GetContact API, пропуская 404 ошибки
    """
    if response_data.get('apiStatusCode') != 200:
        return {}
    
    phone_data = {
        'phone': response_data['data']['request'],
        'sources': {}
    }
    
    for source in response_data['data']['responce']:
        if source['results']['statusCode'] == 404:
            continue
            
        source_name = source['source']
        response = source['results']['response']
        
        if source_name == 'callapp':
            if 'name' in response:
                phone_data['sources']['name'] = response['name']
            if 'addresses' in response:
                phone_data['sources']['addresses'] = [addr['street'] for addr in response['addresses']]
            if 'categories' in response:
                phone_data['sources']['categories'] = [cat['name'] for cat in response['categories']]
            if 'websites' in response:
                phone_data['sources']['websites'] = [site['websiteUrl'] for site in response['websites']]
            if 'facebookID' in response:
                phone_data['sources']['facebook_id'] = response['facebookID']['id']
                
        elif source_name == 'whatsapp':
            if 'businessProfile' in response:
                profile = response['businessProfile']
                phone_data['sources']['business_address'] = profile.get('address', '')
                phone_data['sources']['business_category'] = profile.get('category', '')
                phone_data['sources']['business_description'] = profile.get('description', '')
                phone_data['sources']['business_email'] = profile.get('email', '')
                if 'website' in profile:
                    phone_data['sources']['business_websites'] = [site['url'] for site in profile['website']]
            if 'status' in response:
                phone_data['sources']['whatsapp_status'] = response['status']
                
        elif source_name == 'callerid':
            if 'name' in response:
                phone_data['sources']['caller_name'] = response['name']
                
        elif source_name == 'eyecon':
            if 'contacts' in response:
                phone_data['sources']['contacts'] = [contact['name'] for contact in response['contacts']]
    
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
