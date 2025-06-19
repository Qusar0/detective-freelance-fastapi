import httpx
from sqlalchemy import select

from server.api.conf.config import settings
from server.api.database.database import get_db
from server.api.dao.base import BaseDAO
from server.api.models.models import ServicesBalance


class ServicesBalanceDAO(BaseDAO):
    model = ServicesBalance

    @classmethod
    async def renew_ibhldr_balance(cls, requests_left):
        async with get_db() as db:
            result = await db.execute(
                select(ServicesBalance)
                .filter_by(service_name='Ibhldr')
            )
            ibhldr_balance = result.scalars().first()

            if ibhldr_balance is not None:
                ibhldr_balance.balance = requests_left
                await db.commit()

    @classmethod
    async def renew_tgdev_balance(cls, requests_left):
        async with get_db() as db:
            TgDev_io_balance = await db.execute(
                select(ServicesBalance)
                .filter_by(service_name='tgdev-io')
            )

            if TgDev_io_balance is not None:
                TgDev_io_balance.balance = requests_left
                await db.commit()

    @classmethod
    async def renew_xml_balance(cls, db):
        url = f"http://xmlriver.com/api/get_balance/?user={settings.xml_river_user_id}&key={settings.xml_river_api_key}"

        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            balance = resp.text

        result = await db.execute(
            select(ServicesBalance)
            .filter_by(service_name='Xmlriver'),
        )
        xmlriver_balance = result.scalar_one_or_none()

        if xmlriver_balance:
            xmlriver_balance.balance = balance
            await db.commit()

    @classmethod
    async def renew_lampyre_balance(cls, db):
        token = settings.utils_token
        url = settings.lighthouse_url

        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params={"token": token})

        lampyre_balance = await db.execute(
            select(ServicesBalance)
            .filter_by(service_name='Lampyre')
        )
        lampyre_balance = lampyre_balance.scalars().first()

        if lampyre_balance:
            lampyre_balance.balance = resp.json()['balance']
            await db.commit()

    @classmethod
    async def renew_getcontact_balance(cls, requests_left, db):
        getcontact_balance = await db.execute(
            select(ServicesBalance)
            .filter_by(service_name='GetContact')
        )
        getcontact_balance = getcontact_balance.scalars().first()

        if getcontact_balance:
            getcontact_balance.balance = requests_left
            await db.commit()

    @classmethod
    async def get_service_balance(cls, db, service_name):
        service = await db.execute(
            select(ServicesBalance)
            .filter_by(service_name=service_name)
        )
        service = service.scalars().first()

        if service:
            return service.balance
