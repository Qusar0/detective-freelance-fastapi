from typing import Optional

from server.api.IRBIS_parser.base_irbis_init import BaseAuthIRBIS
from server.api.models.irbis_models import (
    BankruptcyFullTable
)


class Bankruptcy:
    @staticmethod
    async def get_data_preview(person_uuid: str):
        """
        Получение превью данных о банкротстве физического лица.


        Args:
            person_uuid (str): uuid человека

        Returns:
            int: Результат запроса по имени.
            int: Результат запроса по инн.
        """
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-bankrot.json?event=preview")
        response = await BaseAuthIRBIS.get_response(link)

        amount_by_name: Optional[int] = 0
        amount_by_inn: Optional[int] = 0

        if response is not None:
            amount_by_name = response["name"]
            amount_by_inn = response["inn"]

        return amount_by_name, amount_by_inn

    @staticmethod
    async def get_full_data(person_uuid: str, page: int, rows: int, search_type: str):  # noqa: WPS615
        """
        Получение данных о банкротстве физического лица.

        Args:
            person_uuid (str): uuid человека
            page (int): Номер страницы
            rows (int): Количество строк на странице
            search_type (str): Соответствует переключателю 'По полным ФИО/ПоИНН'. Принимает значения 'name', 'inn'

        Returns:
            list: Результат запроса
        """
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-bankrot.json?event=data&"
                f"page={page}&rows={rows}&search_type={search_type}&version=2")
        response = await BaseAuthIRBIS.get_response(link)

        full_data: Optional[list] = []

        if response is not None:
            full_data = response["result"]

        return full_data

    @staticmethod
    async def _process_bankruptcy_data(irbis_person_id: int, person_uuid: str, search_type: str):
        """Обработка данных о банкротстве с пагинацией"""
        full_data = []
        page = 1

        while True:
            data = await Bankruptcy.get_full_data(person_uuid, page, 50, search_type)
            if not data:
                break
            full_data.extend(data)
            page += 1

        test_data = [
            {
                "first_name": "Иван",
                "second_name": "Петрович",
                "last_name": "Сидоров",
                "birth_date": "15.03.1978",
                "born_place": "г. Москва",
                "inn": "771234567890",
                "ogrn": "1234567890123",
                "snils": "123-456-789-00",
                "old_name": "Сидоров-Петров И.П.",
                "category_name": "Индивидуальный предприниматель",
                "location": "Московский областной суд",
                "region_name": "Московская область",
                "information": "Дело о банкротстве № А40-123456/2023",
                "link": "https://bankrot.fedresurs.ru/Card.aspx?ID=abc123def456",
            },
            {
                "first_name": "Мария",
                "second_name": "Сергеевна",
                "last_name": "Иванова",
                "birth_date": "22.07.1985",
                "born_place": "г. Санкт-Петербург",
                "inn": "784512345678",
                "ogrn": "9876543210987",
                "snils": "987-654-321-00",
                "old_name": None,
                "category_name": "Физическое лицо",
                "location": "Арбитражный суд г. Санкт-Петербурга",
                "region_name": "г. Санкт-Петербург",
                "information": "Дело о банкротстве № А56-789012/2024",
                "link": "https://bankrot.fedresurs.ru/Card.aspx?ID=xyz789uvw456",
            }
        ]
        return [
            BankruptcyFullTable(
                irbis_person_id=irbis_person_id,
                first_name=item.get("first_name"),
                second_name=item.get("second_name"),
                last_name=item.get("last_name"),
                birth_date=item.get("birth_date"),
                born_place=item.get("born_place"),
                inn=item.get("inn"),
                ogrn=item.get("ogrn"),
                snils=item.get("snils"),
                old_name=item.get("old_name"),
                category_name=item.get("category_name"),
                location=item.get("location"),
                region_name=item.get("region_name"),
                information=item.get("information"),
                link=item.get("link"),
                search_type=search_type,
            )
            for item in test_data
        ]
