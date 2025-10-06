from typing import Optional

from server.api.IRBIS_parser.base_irbis_init import BaseAuthIRBIS
from server.api.models.irbis_models import (
    DisqualifiedPersonFullTable
)


class DisqualifiedPersons:
    @staticmethod
    async def get_data_preview(person_uuid: str):
        """
        Получение превью данных о дисквалификации физического лица.

        Args:
            person_uuid (str): uuid человека

        Returns:
            int: Результат запроса
        """
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-disqualified.json?event=preview")
        response = await BaseAuthIRBIS.get_response(link)

        count: Optional[int] = 0

        if response is not None:
            count = response

        return count

    @staticmethod
    async def get_full_data(person_uuid: str, page: int, rows: int):  # noqa: WPS615
        """
        Получение данных о дисквалификации физического лица.
        Args:
            person_uuid (str): uuid человека
            page (int): Номер страницы
            rows (int): Количество строк на странице

        Returns:
            list: Результат запроса
        """
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-disqualified.json?event=data"
                f"&page={page}&rows={rows}")
        response = await BaseAuthIRBIS.get_response(link)

        full_data: Optional[list] = []

        if response is not None:
            full_data = response["result"]

        return full_data

    @staticmethod
    async def _process_bankruptcy_data(irbis_person_id: int, person_uuid: str):
        """Обработка данных о банкротстве с пагинацией"""
        full_data = []
        page = 1

        while True:
            data = await DisqualifiedPersons.get_full_data(person_uuid, page, 50)
            if not data:
                break
            full_data.extend(data)
            page += 1

        test_disqualified_data = [
            {
                "birth_date": "12.05.1980",
                "fio": "Петров Сергей Иванович",
                "article": "ст. 14.1 КоАП РФ",
                "start_date_disq": "15.01.2023",
                "end_date_disq": "15.01.2026",
                "bornplace": "г. Екатеринбург",
                "fio_judge": "Иванова Мария Петровна",
                "office_judge": "Арбитражный суд Свердловской области",
                "legal_name": "ООО 'СтройИнвест'",
                "office": "Директор",
                "department": "Территориальный орган Росимущества по Свердловской области"
            },
            {
                "birth_date": "03.11.1975",
                "fio": "Семенов Алексей Владимирович",
                "article": "ст. 14.12 КоАП РФ",
                "start_date_disq": "20.03.2022",
                "end_date_disq": "20.03.2025",
                "bornplace": "г. Новосибирск",
                "fio_judge": "Петров Дмитрий Сергеевич",
                "office_judge": "Арбитражный суд Новосибирской области",
                "legal_name": "ЗАО 'ТехноПром'",
                "office": "Генеральный директор",
                "department": "Управление Федеральной службы по финансовому мониторингу"
            },
            {
                "birth_date": "28.07.1988",
                "fio": "Козлова Анна Дмитриевна",
                "article": "ст. 14.13 КоАП РФ",
                "start_date_disq": "10.09.2024",
                "end_date_disq": "10.09.2027",
                "bornplace": "г. Казань",
                "fio_judge": "Сидорова Ольга Викторовна",
                "office_judge": "Арбитражный суд Республики Татарстан",
                "legal_name": "ООО 'ФинансГрупп'",
                "office": "Главный бухгалтер",
                "department": "Территориальное управление Банка России"
            }
        ]
        return [
            DisqualifiedPersonFullTable(
                irbis_person_id=irbis_person_id,
                birth_date=item.get("birth_date"),
                fio=item.get("fio"),
                article=item.get("article"),
                start_date_disq=item.get("start_date_disq"),
                end_date_disq=item.get("end_date_disq"),
                bornplace=item.get("bornplace"),
                fio_judge=item.get("fio_judge"),
                office_judge=item.get("office_judge"),
                legal_name=item.get("legal_name"),
                office=item.get("office"),
                department=item.get("department")
            )
            for item in test_disqualified_data
        ]
