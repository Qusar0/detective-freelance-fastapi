import asyncio
from typing import Optional

import aiohttp

from server.api.conf.config import settings


class BaseAuthIRBIS:
    def __init__(  # noqa: WPS211
        self,
        first_name: str,
        last_name: str,
        regions: list[int],
        second_name: Optional[str] = None,
        birth_date: Optional[str] = None,
        passport_series: Optional[str] = None,
        passport_number: Optional[str] = None,
        inn: Optional[str] = None,
    ):
        # Обязательные поля
        self._token_id: str = settings.irbis_token
        self._first_name: str = first_name
        self._last_name: str = last_name
        self._regions: list[int] = regions

        # Необязательные поля
        self._second_name: Optional[str] = second_name
        self._birth_date: Optional[str] = birth_date
        self._passport_series: Optional[str] = passport_series
        self._passport_number: Optional[str] = passport_number
        self._inn: Optional[str] = inn

    def generate_link(self):
        temp_dict = {
            "PeopleQuery.LastName": self._last_name,
            "PeopleQuery.FirstName": self._first_name,
            "PeopleQuery.SecondName": self._second_name,
            "PeopleQuery.BirthDate": self._birth_date,
            "regions": self._regions,
            "PeopleQuery.PassportSeries": self._passport_series,
            "PeopleQuery.PassportNumber": self._passport_number,
            "PeopleQuery.INN": self._inn
        }

        result_link_list = [f"https://ir-bis.org/ru/base/-/services/people-check.json?token={self._token_id}"]
        for key, key_value in temp_dict.items():
            if key_value is not None:
                result_link_list.append(f"{key}={key_value}")

        result_link = "&".join(result_link_list)
        return result_link

    async def get_person_uuid(self):
        link = self.generate_link()

        async with aiohttp.ClientSession() as session:
            async with session.get(link) as response:
                response = await response.json()
                if response["status"] == 0:
                    return response["uuid"]
        return None

    @staticmethod
    async def get_response(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as response:
                response_data = await response.json()

            if response_data["status"] == 0:
                await asyncio.sleep(float(response_data["waitTime"]) / 1000)
                async with session.get(link) as repeated_response:
                    response_data = await repeated_response.json()

            if response_data["status"] == 1:
                return response_data["response"]
            else:
                return None
