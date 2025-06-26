from typing import Optional

from server.api.IRBIS_parser.base_irbis_init import BaseAuthIRBIS


class MLIndex:
    def __init__(self):
        self.full_data: Optional[dict] = dict()

    async def get_full_data(self, person_uuid: str):  # noqa: WPS615
        """
        Получение значения ML-индекса данного физического лица. Использовать повторно функцию для обновления данных.
        Если нужны предыдущие, необходимо обратиться к полю full_data

        Args:
            person_uuid (str): uuid человека

        Returns:
            int: Результат запроса
        """
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-scoring.json?event=scoring")
        response = await BaseAuthIRBIS.get_response(link)

        if response is not None:
            self.full_data = response

        return self.full_data
