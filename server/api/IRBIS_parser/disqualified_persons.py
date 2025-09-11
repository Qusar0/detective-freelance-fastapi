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
    async def _process_bankruptcy_data(self, irbis_person_id: int, person_uuid: str):
        """Обработка данных о банкротстве с пагинацией"""
        full_data = []
        page = 1

        while True:
            data = await DisqualifiedPersons.get_full_data(person_uuid, page, 50)
            if not data:
                break
            full_data.extend(data)
            page += 1

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
            for item in full_data
        ]
