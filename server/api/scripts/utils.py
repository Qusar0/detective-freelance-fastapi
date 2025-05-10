from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from server.api.models.models import (
    Keywords,
    ServicesBalance,
    ProhibitedSites,
    Users,
    TelegramNotifications,
    UserQueries,
    UserBalances,
    Events
)
from typing import Dict, Tuple
from server.api.database.database import get_db
import base64
import httpx
from datetime import datetime
from server.api.conf.config import settings


async def get_default_keywords(
    db: AsyncSession,
    default_keywords_type: str,
    count: bool = False,
) -> Tuple[Dict, bool]:
    splitted_kws = default_keywords_type.split(", ")
    named_keywords = {}
    counter = 0

    if '' in splitted_kws:
        return (counter, {}) if count else named_keywords

    if 'report' in splitted_kws:
        types_belongs_report = ['reputation', 'negativ', 'relations']
        for kwd_type in types_belongs_report:
            query = select(Keywords.word).filter_by(word_language='ru', word_type=kwd_type)
            result = await db.execute(query)
            keywords = [kwd.word for kwd in result.scalars()]
            counter += len(keywords)
            named_keywords[kwd_type] = keywords
        return (counter, named_keywords) if not count else counter

    elif 'company_report' in splitted_kws:
        types_belongs_report = ['company_reputation', 'company_negativ', 'company_relations']
        for kwd_type in types_belongs_report:
            query = select(Keywords.word).filter_by(word_language='ru', word_type=kwd_type)
            result = await db.execute(query)
            keywords = [kwd.word for kwd in result.scalars()]
            counter += len(keywords)
            named_keywords[kwd_type] = keywords
        return (counter, named_keywords) if not count else counter

    else:
        for splitted_kwd in splitted_kws:
            query = select(Keywords.word).filter_by(word_language='ru', word_type=splitted_kwd)
            result = await db.execute(query)
            keywords = [kwd.word for kwd in result.scalars()]
            counter += len(keywords)
            named_keywords[splitted_kwd] = keywords

        return (counter, named_keywords) if not count else counter


async def calculate_name_price(
    db: AsyncSession,
    search_patronymic: str,
    keywords: list[str],
    default_keywords_type: str
) -> float:
    NAME_CASES = 5

    len_user_kwds = len(keywords)
    default_kwds = await get_default_keywords(db, default_keywords_type, count=True)
    len_default_kwds = len(default_kwds)

    len_all_keywords = 1 if len_user_kwds + len_default_kwds == 0 else len_user_kwds + len_default_kwds

    if search_patronymic == "":
        fi_default_queries_count = 2 * NAME_CASES
        query_count = fi_default_queries_count * len_all_keywords
    else:
        fio_default_queries_count = 4 * NAME_CASES
        # переменная которая нужна для высчитывания запросов ФИ + слова с списке
        not_to_search = 10 * len_default_kwds
        query_count = (fio_default_queries_count * len_all_keywords) - not_to_search

    price = (query_count * 0.02) * 3
    return round(price, 2)


async def renew_ibhldr_balance(requests_left):
    async with get_db() as db:
        result = await db.execute(
            select(ServicesBalance)
            .filter_by(service_name='Ibhldr')
        )
        ibhldr_balance = result.scalars().first()

        if ibhldr_balance is not None:
            ibhldr_balance.balance = requests_left
            await db.commit()


async def renew_tgdev_balance(requests_left):
    async with get_db() as db:
        TgDev_io_balance = await db.execute(
            select(ServicesBalance)
            .filter_by(service_name='tgdev-io')
        )

        if TgDev_io_balance is not None:
            TgDev_io_balance.balance = requests_left
            await db.commit()


async def add_sites_from_db(user_prohibited_sites: list, db) -> list:
    result = await db.execute(select(ProhibitedSites.site_link))
    sites_from_db = result.scalars().all()

    return list(set(sites_from_db + user_prohibited_sites))


async def generate_sse_message_type(user_id: int, db=None) -> str:
    query = select(Users).filter_by(id=user_id)
    if not db:
        async with get_db() as db:
            result = await db.execute(query)
    else:
        result = await db.execute(query)

    user = result.scalar_one_or_none()

    if user is None:
        raise ValueError(f"User with id {user_id} not found")

    email = user.email
    created_time = str(user.created)

    message_type = f"{email}{created_time}"
    base64_string = base64.b64encode(
        message_type.encode("ascii"),
    ).decode("ascii")

    return base64_string


async def renew_xml_balance(db):
    url = f"{settings.xml_river_url}/api/get_balance/?user={settings.xml_river_user_id}&key={settings.xml_river_api_key}"

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


async def renew_lampyre_balance(db):
    token = settings.utils_token
    url = settings.lampyre_url

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


async def renew_getcontact_balance(requests_left, db):
    getcontact_balance = await db.execute(
        select(ServicesBalance)
        .filter_by(service_name='GetContact')
    )
    getcontact_balance = getcontact_balance.scalars().first()

    if getcontact_balance:
        getcontact_balance.balance = requests_left
        await db.commit()


async def is_user_subscribed_on_tg(user_id, db):
    result = await db.execute(
        select(TelegramNotifications).filter_by(user_id=user_id)
    )
    user = result.scalar_one_or_none()

    return user.chat_id if user else False


async def get_queries_page(filter: tuple, page: int = 0, page_size: int = 20, db: AsyncSession = None):
    stmt = (
        select(UserQueries)
        .filter_by(user_id=filter[0], query_category=filter[1])
        .order_by(UserQueries.query_created_at.desc())
    )

    if page_size:
        stmt = stmt.limit(page_size)
    if page:
        stmt = stmt.offset(page * page_size)

    result = await db.execute(stmt)
    queries = result.scalars().all()

    return queries


async def subtract_balance(user_id: int, amount: float, channel: str, db: AsyncSession):
    from server.__main__ import publish_event
    result = await db.execute(
        select(UserBalances)
        .filter_by(user_id=user_id),
    )
    user_balance = result.scalars().first()

    if not user_balance:
        return

    user_balance.balance = round(
        user_balance.balance + (-amount),
        2,
    )

    await db.commit()

    event_data = {
        "event_type": "balance",
        "balance": user_balance.balance,
    }

    await publish_event(channel, event_data)


async def save_event(data: str, query_id: int, db: AsyncSession):
    now = datetime.now()

    user_query = Events(
        event_type="test",
        query_id=query_id,
        created_time=now,
        additional_data=data,
        event_status="unseen"
    )

    db.add(user_query)
    await db.commit()
    await db.refresh(user_query)

    return user_query.event_id, user_query.event_type, user_query.created_time, user_query.event_status


def calculate_num_price(methods_type):
    price = 0
    if 'mentions' in methods_type:
        price += 5
    if 'bindings' in methods_type:
        price += 65

    return price


def calculate_email_price(methods_type):
    price = 0
    if 'mentions' in methods_type:
        price += 5
    if 'acc search' in methods_type:
        price += 120

    return price


async def save_user_and_chat(user_id, chat_id, db):
    result = await db.execute(
        select(TelegramNotifications).filter_by(user_id=user_id, chat_id=chat_id)
    )
    existing_chat = result.scalar_one_or_none()
    
    if existing_chat:
        return False
        
    db.add(
        TelegramNotifications(
            user_id=user_id,
            chat_id=chat_id,
        ),
    )
    await db.commit()
    return True
