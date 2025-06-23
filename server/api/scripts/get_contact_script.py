import requests
import logging
import re
from server.api.conf.config import settings


class GetContactService:
    """Статический класс для работы с GetContact API"""
    
    @staticmethod
    def _extract_coordinates_from_url(url):
        """Извлекает координаты из Google Maps URL."""
        if 'maps.google.com' in url:
            coord_match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', url)
            if coord_match:
                lat, lon = coord_match.groups()
                return {'lat': float(lat), 'lon': float(lon)}
        return None
    
    @staticmethod
    def _extract_common_fields(response, data):
        """Извлекает общие поля из ответа."""
        if 'description' in response:
            data['description'] = response['description']
        if 'phone' in response:
            data['phone'] = response['phone']
        if 'email' in response:
            data['email'] = response['email']
        if 'avatar' in response and response['avatar']:
            data['avatar'] = response['avatar']
        if 'operator' in response and response['operator']:
            data['operator'] = response['operator']
        if 'country' in response:
            data['country'] = response['country']
        if 'city' in response:
            data['city'] = response['city']
        if 'state' in response:
            data['state'] = response['state']
        if 'company' in response:
            data['company'] = response['company']
        if 'job_title' in response:
            data['job_title'] = response['job_title']
        if 'verified' in response:
            data['verified'] = response['verified']
        if 'spam' in response:
            data['spam'] = response['spam']
        if 'rating' in response:
            data['rating'] = response['rating']
        if 'reviews' in response:
            data['reviews_count'] = response['reviews']
        if 'website' in response:
            data['website'] = response['website']
        if 'social' in response:
            data['social'] = response['social']
        if 'tags' in response:
            data['tags'] = response['tags']
        if 'location' in response:
            data['location'] = response['location']
        if 'fax' in response:
            data['fax'] = response['fax']
        if 'mobile' in response:
            data['mobile'] = response['mobile']
        if 'zip' in response:
            data['zip'] = response['zip']
        return data
    
    @staticmethod
    def _handle_callapp(response):
        """Обрабатывает ответ от сервиса CallApp."""
        data = {}
        
        # Общие поля
        data = GetContactService._extract_common_fields(response, data)
        
        # Специфичные поля CallApp
        if 'name' in response:
            data['name'] = response['name']
        if 'addresses' in response:
            data['addresses'] = [addr['street'] for addr in response['addresses']]
            # Извлекаем координаты из URL адресов
            coordinates = []
            for addr in response['addresses']:
                if 'url' in addr:
                    coord = GetContactService._extract_coordinates_from_url(addr['url'])
                    if coord:
                        coordinates.append(coord)
            if coordinates:
                data['coordinates'] = coordinates
        if 'categories' in response:
            data['categories'] = [cat['name'] for cat in response['categories']]
        if 'websites' in response:
            data['websites'] = [site['websiteUrl'] for site in response['websites']]
        if 'facebookID' in response:
            data['facebook_id'] = response['facebookID']['id']
        return data

    @staticmethod
    def _handle_whatsapp(response):
        """Обрабатывает ответ от сервиса WhatsApp."""
        data = {}
        
        # Общие поля
        data = GetContactService._extract_common_fields(response, data)
        
        # Специфичные поля WhatsApp
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

    @staticmethod
    def _handle_callerid(response):
        """Обрабатывает ответ от сервиса CallerID."""
        data = {}
        
        # Общие поля
        data = GetContactService._extract_common_fields(response, data)
        
        # Специфичные поля CallerID
        if 'name' in response:
            data['caller_name'] = response['name']
        # Проверяем наличие координат в URL
        if 'url' in response:
            coord = GetContactService._extract_coordinates_from_url(response['url'])
            if coord:
                data['coordinates'] = [coord]
        
        # Дополнительные поля, специфичные для CallerID
        if 'photo' in response and response['photo']:
            data['photo'] = response['photo']
        if 'photos' in response:
            data['photos'] = [photo.get('url', '') for photo in response['photos'] if photo.get('url')]
        if 'lastSeen' in response:
            data['last_seen'] = response['lastSeen']
        if 'isBusiness' in response:
            data['is_business'] = response['isBusiness']
        if 'isVerified' in response:
            data['is_verified'] = response['isVerified']
        if 'isBlocked' in response:
            data['is_blocked'] = response['isBlocked']
        if 'businessHours' in response:
            data['business_hours'] = response['businessHours']
        if 'businessAddress' in response:
            data['business_address'] = response['businessAddress']
        if 'businessCategory' in response:
            data['business_category'] = response['businessCategory']
        if 'businessDescription' in response:
            data['business_description'] = response['businessDescription']
        if 'businessEmail' in response:
            data['business_email'] = response['businessEmail']
        if 'businessWebsites' in response:
            data['business_websites'] = response['businessWebsites']
        if 'businessPhoto' in response:
            data['business_photo'] = response['businessPhoto']
        if 'businessCoverPhoto' in response:
            data['business_cover_photo'] = response['businessCoverPhoto']
        if 'businessRating' in response:
            data['business_rating'] = response['businessRating']
        return data

    @staticmethod
    def _handle_eyecon(response):
        """Обрабатывает ответ от сервиса Eyecon."""
        data = {}
        
        # Общие поля
        data = GetContactService._extract_common_fields(response, data)
        
        # Специфичные поля Eyecon
        if 'contacts' in response:
            data['contacts'] = [contact['name'] for contact in response['contacts']]
        return data

    @staticmethod
    def parse_response(response_data):
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
            'callapp': GetContactService._handle_callapp,
            'whatsapp': GetContactService._handle_whatsapp,
            'callerid': GetContactService._handle_callerid,
            'eyecon': GetContactService._handle_eyecon,
        }

        for source in response_data['data']['responce']:
            if source['results']['statusCode'] == 404:
                continue

            source_name = source['source']
            response = source['results']['response']

            if handler := handler_map.get(source_name):
                phone_data['sources'].update(handler(response))

        return phone_data

    @staticmethod
    def get_tags_and_data(number):
        """
        Получает теги и данные из GetContact API для указанного номера.
        
        Args:
            number: Номер телефона для поиска
            
        Returns:
            tuple: (список_тегов, количество_оставшихся_запросов, распарсенные_данные)
        """
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
            
            parsed_data = GetContactService.parse_response(contacs_json)
            return list_tags, requests_left, parsed_data
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            return [], 0, {} 