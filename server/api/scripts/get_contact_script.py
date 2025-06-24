import logging
from server.api.conf.config import settings
import httpx


class GetContactService:
    """Статический класс для работы с GetContact API"""

    @staticmethod
    def _handle_getcontact(response):
        """Обрабатывает ответ от сервиса GetContact."""
        data = {}

        if 'tagCount' in response and response['tagCount'] > 0:
            extra = response.get('extra', [])
            if extra:
                tags = extra['tags']
                data['tags'] = [tag['tag'] for tag in tags if 'tag' in tag]
        else:
            data['tags'] = []

        return data

    @staticmethod
    def _handle_callapp(response):
        """Обрабатывает ответ от сервиса CallApp."""
        data = {}

        if 'name' in response:
            data['name'] = response['name']
        if 'description' in response:
            data['description'] = response['description']
        if 'addresses' in response:
            data['addresses'] = [addr['street'] for addr in response['addresses']]
        if 'url' in response and 'maps.google.com' in response['url']:
            data['map_url'] = response['url']
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

        if 'businessName' in response:
            data['business_name'] = response['businessName']
        if 'status' in response:
            data['status'] = response['status']
        if 'urlAvatar' in response and response['urlAvatar']:
            data['avatar'] = response['urlAvatar']
        if 'businessProfile' in response:
            profile = response['businessProfile']
            if 'address' in profile:
                data['business_address'] = profile['address']
            if 'category' in profile:
                data['business_category'] = profile['category']
            if 'description' in profile:
                data['business_description'] = profile['description']
            if 'email' in profile:
                data['business_email'] = profile['email']
            if 'website' in profile:
                data['business_websites'] = [site['url'] for site in profile['website']]

        return data

    @staticmethod
    def _handle_callerid(response):
        """Обрабатывает ответ от сервиса CallerID."""
        data = {}

        if 'name' in response:
            data['caller_name'] = response['name']
        if 'avatar' in response and response['avatar']:
            data['avatar'] = response['avatar']
        if 'operator' in response and response['operator']:
            data['operator'] = response['operator']
        if 'type' in response and response['type']:
            data['type'] = response['type']
        if 'type_label' in response and response['type_label']:
            data['type_label'] = response['type_label']

        return data

    @staticmethod
    def _handle_eyecon(response):
        """Обрабатывает ответ от сервиса Eyecon."""
        data = {}

        if 'contacts' in response:
            data['contacts'] = [contact['name'] for contact in response['contacts']]
        if 'urlAvatar' in response and response['urlAvatar']:
            data['avatar'] = response['urlAvatar']

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
            'getcontact': GetContactService._handle_getcontact,
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
    async def get_tags_and_data(number):
        """
        Получает данные из GetContact API для указанного номера.
        Args:
            number: Номер телефона для поиска

        Returns:
            tuple: (количество_оставшихся_запросов, распарсенные_данные)
        """
        headers = {
            'x-bot-id': str(settings.telegram_api_id),
            'x-bot-token': str(settings.telegram_api_hash),
            'x-api-key': str(settings.telegram_db_encryption_key),
            'Content-Type': 'application/json',
        }

        try:
            async with httpx.AsyncClient() as client:
                r = await client.post(
                    'https://r0cyk3wpdg.execute-api.us-east-2.amazonaws.com/default/apiv2',
                    headers=headers,
                    json={"phone": str(number)}
                )
                r.raise_for_status()

                contacs_json = r.json()
                requests_left = contacs_json['data']['subscription']['remainingRequestCount']

                parsed_data = GetContactService.parse_response(contacs_json)
                return requests_left, parsed_data

        except httpx.RequestError as e:
            logging.error(f"Request failed: {e}")
            return 0, {}
