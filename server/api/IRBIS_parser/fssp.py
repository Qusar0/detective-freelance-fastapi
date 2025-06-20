from typing import Optional

from .base_irbis_init import BaseAuthIRBIS


class FSSP(BaseAuthIRBIS):
    def __init__(self, first_name: str, last_name: str, regions: list[int],
                 second_name: Optional[str] = None,
                 birth_date: Optional[str] = None,
                 passport_series: Optional[str] = None,
                 passport_number: Optional[str] = None,
                 inn: Optional[str] = None):
        super().__init__(first_name, last_name, regions,
                         second_name, birth_date, passport_series,
                         passport_number, inn)

        self.fssp_preview: Optional[list] = []

        self.full_data: Optional[list] = []

    def get_data_preview(self):
        """
        Получение превью данных об исполнительных производствах, связанных с физическим лицом. Использовать повторно функцию для обновления данных.
        Если нужны предыдущие, необходимо обратиться к полям count

        Returns:
            list: Результат запроса
        """
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{self.person_uuid}/people-fssp.json?event=preview")
        response = self.get_response(link)

        if response is not None:
            self.fssp_preview = response

        return self.fssp_preview

    def get_full_data(self, page: int, rows: int):
        """
        Получение данных об исполнительных производствах, связанных с физическим лицом. Использовать повторно функцию для обновления данных.
        Если нужны предыдущие, необходимо обратиться к полям full_data

         Args:
            page (int): Номер страницы
            rows (int): Количество строк на странице

        Returns:
            list: Результат запроса
        """
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{self.person_uuid}/people-fssp.json?event=data&"
                f"page={page}&rows={rows}")
        response = self.get_response(link)

        if response is not None:
            self.full_data = response["result"]

        return self.full_data
