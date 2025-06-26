from typing import Optional

from server.api.IRBIS_parser.base_irbis_init import BaseAuthIRBIS


class ParticipationOrganization:
    def __init__(self):
        self.all_regions: Optional[list] = []
        self.selected_regions: Optional[list] = []

        self.full_data: Optional[list] = []

    async def get_data_preview(self, person_uuid: str):
        """
        Получение превью данных об участии физического лица в организациях и ИП.
        Если нужны предыдущие, необходимо обратиться к полям all_regions и selected_regions

        Args:
            person_uuid (str): uuid человека

        Returns:
            list: Результат запроса по всем регионам
            list: Результат запроса по выбранным регионам
        """
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-orgs.json?event=preview")
        response = await BaseAuthIRBIS.get_response(link)

        if response is not None:
            self.all_regions = response["all"]
            self.selected_regions = response["selected"]

        return self.all_regions, self.selected_regions

    async def get_full_data(self, person_uuid: str, page: int, rows: int, search_type: str):  # noqa: WPS615
        """
        Получение данных об участии физического лица в организациях и ИП.
        Если нужны предыдущие, необходимо обратиться к полям full_data

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

        if response is not None:
            self.full_data = response["result"]
            return self.full_data
        return []
