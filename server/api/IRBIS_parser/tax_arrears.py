from typing import Optional

from .base_irbis_init import BaseAuthIRBIS


class TaxArrears(BaseAuthIRBIS):
    def __init__(self, first_name: str, last_name: str, regions: list[int],
                 second_name: Optional[str] = None,
                 birth_date: Optional[str] = None,
                 passport_series: Optional[str] = None,
                 passport_number: Optional[str] = None,
                 inn: Optional[str] = None):
        super().__init__(first_name, last_name, regions,
                         second_name, birth_date, passport_series,
                         passport_number, inn)

        self.full_data: Optional[list] = []

    def get_full_data(self):
        """
        Получение данных о налоговых задолженностях физического лица. Использовать повторно функцию для обновления данных.
        Если нужны предыдущие, необходимо обратиться к полям full_data

        Returns:
            list: Результат запроса
        """
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{self.person_uuid}/people-nalog.json?event=data")
        response = self.get_response(link)

        if response is not None:
            self.full_data = response["payload"]

        return self.full_data
