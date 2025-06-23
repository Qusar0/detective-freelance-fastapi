from typing import Optional

from .base_irbis_init import BaseAuthIRBIS


class PassportCheck:
    def __init__(self):
        self.valid: Optional[bool] = False

    async def is_valid(self, person_uuid: str):
        """
        Проверка серии и номера паспорта на действительность. Использовать повторно функцию для обновления данных.
        Если нужны предыдущие, необходимо обратиться к полям valid

        Args:
            person_uuid (str): uuid человека

        Returns:
            bool: Результат запроса
        """
        link = (f"http://ir-bis.org/ru/base/-/services/report/"
                f"{person_uuid}/people-passport.json?event=result")
        response = await BaseAuthIRBIS.get_response(link)

        if response is not None:
            self.valid = bool(response)

        return self.valid
