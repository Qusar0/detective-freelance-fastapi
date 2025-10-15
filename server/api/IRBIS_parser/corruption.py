from typing import Optional

from server.api.IRBIS_parser.base_irbis_init import BaseAuthIRBIS
from server.api.models.irbis_models import CorruptionFullTable


class Corruption:

    @staticmethod
    async def get_data_preview(person_uuid: str):
        """
        Получение превью данных о причастии к коррупционной деятельности физического лица.

        Args:
            person_uuid (str): uuid человека

        Returns:
            int: Результат запроса
        """
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-corrupt.json?event=preview")
        response = await BaseAuthIRBIS.get_response(link)

        count: Optional[int] = 0

        if response is not None:
            count = response["count"]

        return count

    @staticmethod
    async def get_full_data(person_uuid: str, page: int, rows: int):  # noqa: WPS615
        """
        Получение данных о причастии к коррупционной деятельности физического лица.

        Args:
            person_uuid (str): uuid человека
            page (int): Номер страницы
            rows (int): Количество строк на странице

        Returns:
            list: Результат запроса
        """
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-corrupt.json?event=data&"
                f"page={page}&rows={rows}")
        response = await BaseAuthIRBIS.get_response(link)

        full_data: Optional[list] = []

        if response is not None:
            full_data = response["result"]

        return full_data

    @staticmethod
    async def _process_corruption_data(irbis_person_id: int, person_uuid: str):
        """Обработка данных о коррупции с пагинацией"""
        full_data = []
        page = 1

        while True:
            data = await Corruption.get_full_data(person_uuid, page, 50)
            if not data:
                break
            full_data.extend(data)
            page += 1

        return [
            CorruptionFullTable(
                irbis_person_id=irbis_person_id,
                full_name=item.get("full_name"),
                organization=item.get("organization"),
                position=item.get("position"),
                normative_act=item.get("normative_act"),
                application_date=item.get("application_date"),
                publish_date=item.get("publish_date"),
                excluded_reason=item.get("excluded_reason")
            )
            for item in full_data
        ]
