from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

# price
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



# price
def calculate_num_price(methods_type):
    price = 0
    if 'mentions' in methods_type:
        price += 5
    if 'tags' in methods_type:
        price += 20

    return price

# price
def calculate_email_price(methods_type):
    price = 0
    if 'mentions' in methods_type:
        price += 5
    if 'acc search' in methods_type:
        price += 120

    return price