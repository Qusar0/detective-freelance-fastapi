# from server.api.conf.config import settings
from time import sleep
from typing import Optional
import requests


class BaseAuthIRBIS:
    def __init__(self, first_name: str, last_name: str, regions: list[int],
                 second_name: Optional[str] = None, birth_date: Optional[str] = None,
                 passport_series: Optional[str] = None, passport_number: Optional[str] = None,
                 inn: Optional[str] = None):
        # Обязательные поля
        self._token_id: str = "settings.irbis_token"
        self._first_name: str = first_name
        self._last_name: str = last_name
        self._regions: list[int] = regions

        # Необязательные поля
        self._second_name: Optional[str] = second_name
        self._birth_date: Optional[str] = birth_date
        self._passport_series: Optional[str] = passport_series
        self._passport_number: Optional[str] = passport_number
        self._inn: Optional[str] = inn

        self.person_uuid: Optional[str] = self.get_person_uuid()

    def generate_link(self):
        temp_dict = {"PeopleQuery.LastName": self._last_name, "PeopleQuery.FirstName": self._first_name,
                     "PeopleQuery.SecondName": self._second_name, "PeopleQuery.BirthDate": self._birth_date,
                     "regions": self._regions, "PeopleQuery.PassportSeries": self._passport_series,
                     "PeopleQuery.PassportNumber": self._passport_number, "PeopleQuery.INN": self._inn}

        result = [f"https://ir-bis.org/ru/base/-/services/people-check.json?token={self._token_id}"]
        for key, value in temp_dict.items():
            if value is not None:
                result.append(f"{key}={value}")

        result_link = "&".join(result)
        return result_link

    def get_person_uuid(self):
        link = self.generate_link()

        r = requests.get(link)
        response = r.json()
        if response["status"] == 0:
            return response["uuid"]
        return None

    @staticmethod
    def get_response(link):
        r = requests.get(link)
        response = r.json()

        while response["status"] == 0:
            sleep(float(response["waitTime"])/1000)
            r = requests.get(link)
            response = r.json()

        if response["status"] == 1:
            return response["response"]
        else:
            return None


if __name__ == '__main__':
    test = BaseAuthIRBIS("Иван", "Иванов",[1, 2], )
    print(test.generate_link())
