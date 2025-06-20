from typing import Optional

from .base_irbis_init import BaseAuthIRBIS


class Bankruptcy(BaseAuthIRBIS):
    def __init__(self, first_name: str, last_name: str, regions: list[int],
                 second_name: Optional[str] = None,
                 birth_date: Optional[str] = None,
                 passport_series: Optional[str] = None,
                 passport_number: Optional[str] = None,
                 inn: Optional[str] = None):
        super().__init__(first_name, last_name, regions,
                         second_name, birth_date, passport_series,
                         passport_number, inn)

        self.amount_by_name: Optional[int] = 0
        self.amount_by_inn: Optional[int] = 0

        self.full_data: Optional[list] = []

    def get_data_preview(self):
        """
        Получение превью данных о банкротстве физического лица. Использовать повторно функцию для обновления данных.
        Если нужны предыдущие, необходимо обратиться к полям amount_by_name и amount_by_inn

        Returns:
            int: Результат запроса по имени.
            int: Результат запроса по инн.
        """
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{self.person_uuid}/people-bankrot.json?event=preview")
        response = self.get_response(link)

        if response is not None:
            self.amount_by_name = response["name"]
            self.amount_by_inn = response["inn"]

        return self.amount_by_name, self.amount_by_inn

    def get_full_data(self, page: int, rows: int, search_type: str):
        """
        Получение данных о банкротстве физического лица. Использовать повторно функцию для обновления данных.
        Если нужны предыдущие, необходимо обратиться к полям full_data

         Args:
            page (int): Номер страницы
            rows (int): Количество строк на странице
            search_type (str): Соответствует переключателю 'По полным ФИО/ПоИНН'. Может принимать значения ['name', 'inn'] для поиска по имени и инн соответственно.

        Returns:
            list: Результат запроса
        """
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{self.person_uuid}/people-bankrot.json?event=data&"
                f"page={page}&rows={rows}&search_type={search_type}&version=2")
        response = self.get_response(link)

        if response is not None:
            self.full_data = response["result"]

        return self.full_data
