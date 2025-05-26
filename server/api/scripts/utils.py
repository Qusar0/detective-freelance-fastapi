from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from server.api.models.models import (
    Keywords,
    ServicesBalance,
    ProhibitedSites,
    Users,
    TelegramNotifications,
    UserQueries,
    UserBalances,
    Events,
    Language,
    CountryLanguage,
)
from typing import Dict, List, Any
from server.api.database.database import get_db
import base64
import httpx
from datetime import datetime
from deep_translator import GoogleTranslator
from server.api.conf.config import settings
from server.api.scripts.sse_manager import publish_event


def process_text(text: str, lang: str) -> str:
    """Обрабатывает и переводит текст с приведением к правильному регистру"""
    if not text:
        return ''
    translated = translate_text(text, 'ru', lang)[0]
    return translated.replace("-", " ").title().replace(" ", "-")


def process_keywords(keywords: List[str], lang: str) -> List[str]:
    """Переводит список ключевых слов"""
    return translate_words({"keywords": keywords}, [lang])


def process_special_field(text: str, prefix: str, lang: str) -> str:
    """Обрабатывает специальные поля (plus/minus) с разделителями"""
    if not text:
        return ''
    terms = text[len(prefix):].split(prefix)
    translated_terms = [translate_text(term, 'ru', lang)[0] for term in terms if term]
    return prefix + prefix.join(translated_terms) if translated_terms else ''


async def translate_name_fields(data: Dict[str, Any], target_languages: List[str]) -> Dict[str, Any]:
    """Переводит все текстовые поля на указанные языки"""
    translated = {
        "name": {},
        "surname": {},
        "patronymic": {},
        "plus": {},
        "minus": {},
        "keywords": {}
    }
    for lang in target_languages:
        translated["name"][lang] = process_text(data["name"], lang)
        translated["surname"][lang] = process_text(data["surname"], lang)
        translated["patronymic"][lang] = process_text(data["patronymic"], lang)
        
        translated["plus"][lang] = process_special_field(data["plus"], '+', lang)
        translated["minus"][lang] = process_special_field(data["minus"], '+-', lang)
        
        translated["keywords"][lang] = process_keywords(data["keywords"], lang)[lang]

    translated["name"]['original'] = data["name"]
    translated["surname"]['original'] = data["surname"]
    translated["patronymic"]['original'] = data["patronymic"]
    translated["plus"]['original'] = data["plus"]
    translated["minus"]['original'] = data["minus"]
    translated["keywords"]['original'] = data["keywords"]

    return translated


async def translate_company_fields(data: Dict[str, Any], target_languages: List[str]) -> Dict[str, Any]:
    """Переводит поля для поиска компании на указанные языки"""
    translated = {
        "location": {},
        "keywords": {},
        "plus": {},
        "minus": {}
    }

    for lang in target_languages:
        translated["location"][lang] = process_text(data["location"], lang)
        
        translated["keywords"][lang] = process_keywords(data["keywords"], lang)[lang]
        
        translated["plus"][lang] = process_special_field(data["plus"], '+', lang)
        
        translated["minus"][lang] = process_special_field(data["minus"], '+-', lang)

    translated["location"]['original'] = data["location"]
    translated["keywords"]['original'] = data["keywords"]
    translated["plus"]['original'] = data["plus"]
    translated["minus"]['original'] = data["minus"]

    return translated


def translate_text(text: str, source_lang: str, target_lang: str) -> List[str]:
    """Функция для перевода текста с разделением по точкам"""
    try:
        translated = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
        return list(set([word.strip().lower() for word in translated.split('. ') if word.strip()]))
    except Exception as e:
        print(f"Translation error for '{text}' to '{target_lang}': {e}")
        return []


def translate_words(
    keywords_by_category: Dict[str, List[str]],
    target_languages: List[str],
    source_language: str = 'ru',
) -> Dict[str, List[str]]:
    translations = {}
    if not target_languages:
        target_languages = ['ru']
    
    for lang in target_languages:
        translations[lang] = {}
        for category, words in keywords_by_category.items():
            text_to_translate = '. '.join(words)
            
            translated_words = translate_text(text_to_translate, source_language, lang)
            translations[lang][category] = list(set(translated_words))
    
    return translations


async def get_countries_code_by_languages(
    db: AsyncSession,
    language_codes: List[str] = None,
) -> Dict[str, List[int]]:
    """Получает коды стран, связанных с указанными языками."""
    if not language_codes:
        language_codes = ['ru']
    
    query = (
        select(CountryLanguage)
        .join(CountryLanguage.language)
        .join(CountryLanguage.country)
        .where(Language.code.in_(language_codes))
        .options(
            joinedload(CountryLanguage.language),
            joinedload(CountryLanguage.country)
        )
    )
    
    result = await db.execute(query)
    country_links = result.scalars().all()
    
    result_dict = {}
    for link in country_links:
        lang_code = link.language.code
        if lang_code not in result_dict:
            result_dict[lang_code] = []
        result_dict[lang_code].append(link.country.country_id)
    
    return result_dict


async def get_languages_by_code(
    db: AsyncSession,
    language_codes: List[str] = None,
) -> List[dict]:
    """Получает информацию о языках по их кодам."""
    if not language_codes:
        language_codes = ['ru']

    query = (
        select(Language)
        .where(Language.code.in_(language_codes))
    )
    
    result = await db.execute(query)
    languages = result.scalars().all()
    
    return [lang.russian_name for lang in languages]

async def get_default_keywords(
    db: AsyncSession,
    default_keywords_type: str,
    languages: List[str] = None,
    count: bool = False,
):
    if not languages:
        languages = ['ru']
    splitted_kws = default_keywords_type.split(", ")
    named_keywords = {}
    counter = 0

    if '' in splitted_kws:
        return (counter, {lang: {} for lang in languages})

    if 'report' in splitted_kws:
        types_belongs_report = ['reputation', 'negativ', 'relations']
        for kwd_type in types_belongs_report:
            query = select(Keywords.word).filter_by(word_type=kwd_type)
            result = await db.execute(query)
            keywords = [kwd for kwd in result.scalars()]
            counter += len(keywords)
            named_keywords[kwd_type] = keywords
    elif 'company_report' in splitted_kws:
        types_belongs_report = ['company_reputation', 'company_negativ', 'company_relations']
        for kwd_type in types_belongs_report:
            query = select(Keywords.word).filter_by(word_type=kwd_type)
            result = await db.execute(query)
            keywords = [kwd for kwd in result.scalars()]
            counter += len(keywords)
            named_keywords[kwd_type] = keywords
    else:
        for splitted_kwd in splitted_kws:
            query = select(Keywords.word).filter_by(word_type=splitted_kwd)
            result = await db.execute(query)
            keywords = [kwd for kwd in result.scalars()]
            counter += len(keywords)
            named_keywords[splitted_kwd] = keywords

    translated_words = translate_words(
        keywords_by_category=named_keywords,
        target_languages=languages,
    )
    coefficient = len(languages) or 1
    return (counter * coefficient, translated_words)


async def calculate_name_price(
    db: AsyncSession,
    search_patronymic: str,
    keywords: List[str],
    default_keywords_type: str,
    languages: List[str],
) -> float:
    NAME_CASES = 5

    len_user_kwds = len(keywords)
    default_kwds = await get_default_keywords(db, default_keywords_type, languages, count=True)
    len_default_kwds = default_kwds[0]

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


async def renew_lampyre_balance(db):
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


async def renew_getcontact_balance(requests_left, db):
    getcontact_balance = await db.execute(
        select(ServicesBalance)
        .filter_by(service_name='GetContact')
    )
    getcontact_balance = getcontact_balance.scalars().first()

    if getcontact_balance:
        getcontact_balance.balance = requests_left
        await db.commit()


async def get_service_balance(db, service_name):
    service = await db.execute(
        select(ServicesBalance)
        .filter_by(service_name=service_name)
    )
    service = service.scalars().first()

    if service:
        return service.balance

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
    if 'tags' in methods_type:
        price += 20

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
