from typing import Optional

from server.api.IRBIS_parser.base_irbis_init import BaseAuthIRBIS


class ParticipationOrganization:
    @staticmethod
    async def get_data_preview(person_uuid: str):
        """
        Получение превью данных об участии физического лица в организациях и ИП.

        Args:
            person_uuid (str): uuid человека

        Returns:
            list: Результат запроса по всем регионам
            list: Результат запроса по выбранным регионам
        """
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-orgs.json?event=preview")
        response = await BaseAuthIRBIS.get_response(link)

        all_regions: Optional[list] = []
        selected_regions: Optional[list] = []

        if response is not None:
            all_regions = response["all"]
            selected_regions = response["selected"]

        return all_regions, selected_regions

    @staticmethod
    async def get_full_data(person_uuid: str, page: int, rows: int, search_type: str):  # noqa: WPS615
        """
        Получение данных об участии физического лица в организациях и ИП.

        Args:
            person_uuid (str): uuid человека
            page (int): Номер страницы
            rows (int): Количество строк на странице
            search_type (str): Переключатель "Все регионы/Только выбранные регионы". Принимает 'selected', 'all'

        Returns:
            list: Результат запроса
        """
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-orgs.json?event=data&"
                f"search_type={search_type}&page={page}&rows={rows}&version=3")
        response = await BaseAuthIRBIS.get_response(link)

        full_data: Optional[list] = []

        if response is not None:
            full_data = response["result"]
        return full_data
