from typing import Optional

from server.api.IRBIS_parser.base_irbis_init import BaseAuthIRBIS


class TaxArrears:
    def __init__(self):
        self.full_data: Optional[list] = []

    async def get_full_data(self, person_uuid: str):  # noqa: WPS615
        """
        Получение данных о налоговых задолженностях физического лица.
        Если нужны предыдущие, необходимо обратиться к полям full_data

        Args:
            person_uuid (str): uuid человека

        Returns:
            list: Результат запроса
        """
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-nalog.json?event=data")
        response = await BaseAuthIRBIS.get_response(link)

        if response is not None:
            self.full_data = response["payload"]

        return self.full_data
