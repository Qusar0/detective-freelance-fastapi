from loguru import logger
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from fastapi.responses import PlainTextResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import MissingTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from typing import List, Union
from server.api.scripts.sse_manager import generate_sse_message_type
from server.api.services.price import calculate_email_price, calculate_name_price, calculate_num_price
from server.bots.notification_bot import BalanceNotifier
from server.api.database.database import get_db
from server.api.models.models import (
    UserQueries,
    Events,
    TextData,
    Language,
)
from server.api.schemas.query import (
    QueriesCountResponse,
    QueryData,
    FindByNameModel,
    FindByNumberModel,
    FindByEmailModel,
    FindByCompanyModel,
    CalculatePriceRequest,
    PriceResponse,
    DownloadQueryRequest,
    FindByIRBISModel,
    QueryDataResponse,
    QueryDataRequest,
    CategoryQueryDataRequest,
    GenerarQueryDataResponse,
    QueryDataResult,
    NameQueryDataResponse,
    NameQueryDataResult,
)

from server.api.dao.queries_balance import QueriesBalanceDAO
from server.api.dao.user_queries import UserQueriesDAO
from server.api.dao.user_balances import UserBalancesDAO
from server.api.dao.balance_history import BalanceHistoryDAO
from server.api.dao.queries_data import QueriesDataDAO
from server.api.dao.query_translation_languages import QueryTranslationLanguagesDAO
from server.api.dao.query_search_category import QuerySearchCategoryDAO
from server.api.dao.additional_query_word import AdditionalQueryWordDAO
from server.api.dao.query_keyword_stats import QueryKeywordStatsDAO
from server.api.services.file_storage import FileStorageService, get_file_storage
from server.api.services.text import translate_name_fields, translate_company_fields
from server.tasks.search.company import start_search_by_company
from server.tasks.search.email import start_search_by_email
from server.tasks.search.irbis import start_search_by_irbis
from server.tasks.search.name import start_search_by_name
from server.tasks.search.number import start_search_by_num


router = APIRouter(
    prefix="/queries",
    tags=["Query"]
)


@router.post("/delete_query")
async def delete_query(
    query_id: int = Query(..., description="ID запроса для удаления"),
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
    file_storage: FileStorageService = Depends(get_file_storage),
):
    try:
        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())

        user_query = await UserQueriesDAO.get_query_by_id(user_id, query_id, db)
        if not user_query:
            raise HTTPException(status_code=404, detail="Запрос не найден или недоступен")

        text_data_result = await db.execute(
            select(TextData)
            .where(TextData.query_id == query_id)
        )
        text_data = text_data_result.scalar_one_or_none()

        if text_data and text_data.file_path:
            await file_storage.delete_query_data(text_data.file_path)

        await db.execute(
            delete(TextData)
            .where(TextData.query_id == query_id),
        )
        await db.execute(
            delete(Events)
            .where(Events.query_id == query_id),
        )
        await db.delete(user_query)
        await db.commit()
        return {"message": "Success"}
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}, статус: {e.status_code}")
        await db.rollback()
        raise e
    except MissingTokenError:
        logger.error('Неавторизованный пользователь')
        await db.rollback()
        raise HTTPException(status_code=401, detail="Неавторизованный пользователь")
    except Exception as e:
        logger.error(f"Ошибка удаления query {query_id}: {str(e)}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Database operation failed")


@router.get("/queries_count", response_model=QueriesCountResponse)
async def queries_count(
    query_category: str,
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    try:
        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())

        result = await db.execute(
            select(UserQueries)
            .where(
                UserQueries.user_id == user_id,
                UserQueries.query_category == query_category,
                UserQueries.deleted_at == None  # noqa: E711
            )
        )
        count = len(result.fetchall())
        return {"count": count}
    except MissingTokenError:
        logger.error('Неавторизованный пользователь')
        raise HTTPException(status_code=401, detail="Неавторизованный пользователь")
    except Exception as e:
        logger.error(f"Failed to count queries: {e}")
        raise HTTPException(status_code=500, detail="Failed to count queries")


@router.get("/query_getter", response_model=List[QueryData])
async def send_query_data(
    query_category: str = Query(..., description="Категория запроса"),
    page: int = Query(0),
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    try:
        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())

        user_queries = await UserQueriesDAO.get_queries_page(user_id, query_category, page, db=db)

        result_list = []

        for q in user_queries:
            result_list.append(
                QueryData(
                    query_id=q.query_id,
                    query_title=q.query_title,
                    query_created_at=q.query_created_at.strftime('%Y/%m/%d %H:%M:%S'),
                    query_status=q.query_status,
                    balance=q.queries_balances.balance,
                ),
            )
        return result_list
    except MissingTokenError:
        logger.error('Неавторизованный пользователь')
        raise HTTPException(status_code=401, detail="Неавторизованный пользователь")
    except Exception as e:
        logger.error(f"Failed to get query data: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve query data")


@router.post("/find_by_name")
@BalanceNotifier.notify_balance
async def find_by_name(
    request_data: FindByNameModel,
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    try:
        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())

        original_data = {
            "name": request_data.search_name.strip(),
            "surname": request_data.search_surname.strip(),
            "patronymic": request_data.search_patronymic.strip(),
            "plus": request_data.search_plus.strip(),
            "minus": request_data.search_minus.strip(),
            "keywords": request_data.keywords
        }

        languages = request_data.languages or ['ru']

        default_keywords_type = request_data.default_keywords_type.strip()
        search_engines = request_data.search_engines

        translated_data = await translate_name_fields(original_data, languages)

        channel = await generate_sse_message_type(user_id=user_id, db=db)

        price = await calculate_name_price(
            db,
            original_data["patronymic"],
            original_data["keywords"],
            default_keywords_type,
            languages,
        )

        query_title = f"{original_data['surname']} {original_data['name']} {original_data['patronymic']}"
        user_query_id = await UserQueriesDAO.save_user_query(user_id, query_title, 'name', db)

        search_filters = (
            translated_data["name"],
            translated_data["surname"],
            translated_data["patronymic"],
            translated_data["plus"],
            translated_data["minus"],
            translated_data["keywords"],
            default_keywords_type,
            user_query_id,
            price,
            search_engines,
            languages
        )

        await UserBalancesDAO.subtract_balance(user_id, price, channel, db)

        await BalanceHistoryDAO.save_payment_to_history(price, user_query_id, db)
        await QueriesBalanceDAO.save_query_balance(user_query_id, price, db)

        start_search_by_name.apply_async(args=(search_filters,), queue='name_tasks')
    except MissingTokenError:
        logger.error('Неавторизованный пользователь')
        raise HTTPException(status_code=401, detail="Неавторизованный пользователь")
    except Exception as e:
        logger.error(f"Failed to process the query: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.post("/find_by_number")
@BalanceNotifier.notify_balance
async def find_by_number(
    request_data: FindByNumberModel,
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    try:
        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())

        search_number = request_data.search_number.strip()
        methods_type = request_data.methods_type

        channel = await generate_sse_message_type(user_id=user_id, db=db)

        price = calculate_num_price(methods_type)

        user_query_id = await UserQueriesDAO.save_user_query(user_id, search_number, 'number', db)

        await UserBalancesDAO.subtract_balance(user_id, price, channel, db)

        await BalanceHistoryDAO.save_payment_to_history(price, user_query_id, db)
        await QueriesBalanceDAO.save_query_balance(user_query_id, price, db)

        start_search_by_num.apply_async(
            args=(search_number, methods_type, user_query_id, price),
            queue='num_tasks'
        )
    except MissingTokenError:
        logger.error('Неавторизованный пользователь')
        raise HTTPException(status_code=401, detail="Неавторизованный пользователь")
    except Exception as e:
        logger.error(f"Failed to process the query: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.post("/find_by_email")
@BalanceNotifier.notify_balance
async def find_by_email(
    request_data: FindByEmailModel,
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    try:
        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())

        search_email = request_data.email.strip()
        methods_type = request_data.methods_type

        channel = await generate_sse_message_type(user_id=user_id, db=db)

        price = calculate_email_price(methods_type)

        user_query_id = await UserQueriesDAO.save_user_query(user_id, search_email, 'email', db)

        await UserBalancesDAO.subtract_balance(user_id, price, channel, db)

        await BalanceHistoryDAO.save_payment_to_history(price, user_query_id, db)
        await QueriesBalanceDAO.save_query_balance(user_query_id, price, db)

        start_search_by_email.apply_async(
            args=(search_email, methods_type, user_query_id, price),
            queue='email_tasks',
        )
    except MissingTokenError:
        logger.error('Неавторизованный пользователь')
        raise HTTPException(status_code=401, detail="Неавторизованный пользователь")
    except Exception as e:
        logger.error(f"Failed to process the query: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.post("/find_by_company")
@BalanceNotifier.notify_balance
async def find_by_company(
    request_data: FindByCompanyModel,
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    try:
        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())

        original_data = {
            "company_name": request_data.company_name.strip(),
            "extra_name": request_data.extra_name.strip(),
            "location": request_data.location.strip(),
            "keywords": request_data.keywords,
            "plus": request_data.search_plus.strip(),
            "minus": request_data.search_minus.strip()
        }

        languages = request_data.languages or ['ru']
        default_keywords_type = request_data.default_keywords_type.strip()
        search_engines = request_data.search_engines

        translated_data = await translate_company_fields(original_data, languages)

        channel = await generate_sse_message_type(user_id=user_id, db=db)
        price = 10

        query_title = original_data['company_name']
        user_query_id = await UserQueriesDAO.save_user_query(user_id, query_title, 'company', db)

        search_filters = (
            query_title,
            original_data['extra_name'],
            translated_data['location'],
            translated_data['keywords'],
            default_keywords_type,
            translated_data['plus'],
            translated_data['minus'],
            user_query_id,
            price,
            search_engines,
            languages
        )

        await UserBalancesDAO.subtract_balance(user_id, price, channel, db)

        await BalanceHistoryDAO.save_payment_to_history(price, user_query_id, db)
        await QueriesBalanceDAO.save_query_balance(user_query_id, price, db)

        start_search_by_company.apply_async(args=(search_filters,), queue='company_tasks')
    except MissingTokenError:
        logger.error('Неавторизованный пользователь')
        raise HTTPException(status_code=401, detail="Неавторизованный пользователь")
    except Exception as e:
        logger.error(f"Failed to process the query: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.post("/find_by_irbis")
@BalanceNotifier.notify_balance
async def find_by_irbis(
    request_data: FindByIRBISModel,
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    try:
        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())

        channel = await generate_sse_message_type(user_id=user_id, db=db)
        price = 100

        query_title = " ".join([request_data.first_name.strip(), request_data.last_name.strip()])

        user_query_id = await UserQueriesDAO.save_user_query(user_id, query_title, 'irbis', db)

        search_filters = {
            "query_id": user_query_id,
            "price": price,
            "first_name": request_data.first_name,
            "last_name": request_data.last_name,
            "regions": request_data.regions,
            "second_name": request_data.second_name,
            "birth_date": request_data.birth_date,
            "passport_series": request_data.passport_series,
            "passport_number": request_data.passport_number,
            "inn": request_data.inn
        }

        await UserBalancesDAO.subtract_balance(user_id, price, channel, db)

        await BalanceHistoryDAO.save_payment_to_history(price, user_query_id, db)
        await QueriesBalanceDAO.save_query_balance(user_query_id, price, db)

        start_search_by_irbis.apply_async(args=(search_filters,), queue='irbis_tasks')
    except MissingTokenError:
        logger.error('Неавторизованный пользователь')
        raise HTTPException(status_code=401, detail="Неавторизованный пользователь")
    except Exception as e:
        logger.error(f"Failed to process the query: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.post("/calculate_price", response_model=PriceResponse)
async def calculate_price(
    data: CalculatePriceRequest,
    db: AsyncSession = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    try:
        Authorize.jwt_required()
        price = await calculate_name_price(
            db,
            data.search_patronymic.strip(),
            data.keywords,
            data.default_keywords_type.strip(),
            data.languages,
        )
        return {"price": price}
    except MissingTokenError:
        logger.error('Неавторизованный пользователь')
        raise HTTPException(status_code=401, detail="Неавторизованный пользователь")
    except Exception as e:
        logger.warning(f"Invalid input: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.post("/download_query", response_class=PlainTextResponse)
async def download_query(
    data: DownloadQueryRequest,
    db: AsyncSession = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    file_storage: FileStorageService = Depends(get_file_storage),
):
    try:
        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())

        query_id = data.query_id
        query = await UserQueriesDAO.get_query_by_id(
            user_id,
            query_id,
            db,
        )
        if not query:
            raise HTTPException(status_code=404, detail="Запрос не найден или недоступен")

        text_result = await db.execute(
            select(TextData.file_path)
            .where(TextData.query_id == query_id)
        )
        file_path = text_result.scalar_one_or_none()

        if not file_path:
            raise HTTPException(status_code=404, detail="Query data not found")

        query_text = await file_storage.get_query_data(file_path)

        return PlainTextResponse(content=query_text, media_type='text/plain; charset=UTF-8')
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}, статус: {e.status_code}")
        raise e
    except MissingTokenError:
        logger.error('Неавторизованный пользователь')
        raise HTTPException(status_code=401, detail="Неавторизованный пользователь")
    except Exception as e:
        logger.error(f"Ошибка при скачивании запроса: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.get("/available_languages")
async def get_available_languages(
    db: AsyncSession = Depends(get_db),
):
    try:
        result = await db.execute(
            select(
                Language.russian_name,
                Language.code,
            ).order_by(Language.russian_name),
        )
        languages = result.fetchall()

        translated = {russian_name: code for russian_name, code in languages}

        return translated
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}, статус: {e.status_code}")
        raise e
    except MissingTokenError:
        logger.error('Неавторизованный пользователь')
        raise HTTPException(status_code=401, detail="Неавторизованный пользователь")
    except Exception as e:
        logger.error(f"Не удалось получить языки: {e}")
        raise HTTPException(status_code=500, detail="Ошибка получения языков")


@router.post("/query_data", response_model=List[Union[NameQueryDataResult, QueryDataResult]])
async def get_query_data(
    request_data: QueryDataRequest = Body(...),
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Получает данные о выполненном запросе с фильтрацией по категориям."""
    try:
        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())

        query = await UserQueriesDAO.get_query_by_id(
            user_id,
            request_data.query_id,
            db,
        )
        if not query:
            raise HTTPException(status_code=404, detail="Запрос не найден или недоступен")

        query_data = await QueriesDataDAO.get_paginated_query_data(
            query_id=request_data.query_id,
            page=request_data.page,
            size=request_data.size,
            keyword_type_category=request_data.keyword_type_category,
            db=db
        )

        results = []
        for data_item, keyword_type in query_data:
            if query.query_category in {'name', 'company'}:
                keyword_type_name = keyword_type.keyword_type_name
                resource_type = data_item.resource_type
            else:
                keyword_type_name = None
                resource_type = None

            keywords_list = [
                kw_assoc.original_keyword.word
                for kw_assoc in data_item.keywords
                if kw_assoc.original_keyword
            ]

            if query.query_category != 'name':
                query_data = QueryDataResult(
                    title=data_item.title,
                    info=data_item.info,
                    url=data_item.link,
                    publication_date=data_item.publication_date,
                    keyword_type_name=keyword_type_name,
                    keywords=keywords_list,
                    resource_type=resource_type,
                )
            else:
                query_data = NameQueryDataResult(
                    title=data_item.title,
                    info=data_item.info,
                    url=data_item.link,
                    publication_date=data_item.publication_date,
                    keyword_type_name=keyword_type_name,
                    keywords=keywords_list,
                    resource_type=resource_type,
                    is_fullname=data_item.is_fullname,
                )

            results.append(query_data)
        return results
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}, статус: {e.status_code}")
        raise e
    except MissingTokenError:
        logger.error('Неавторизованный пользователь')
        raise HTTPException(status_code=401, detail="Неавторизованный пользователь")
    except Exception as e:
        logger.error(f"Ошибка при получении данных запроса {request_data.query_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Произошла ошибка при получении данных запроса",
        )


@router.post("/category_query_data", response_model=Union[NameQueryDataResponse, QueryDataResponse])
async def get_category_query_data(
    request_data: CategoryQueryDataRequest = Body(...),
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Получает данные о выполненном запросе с фильтрацией по категориям."""
    try:
        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())

        query = await UserQueriesDAO.get_query_by_id(
            user_id,
            request_data.query_id,
            db,
        )
        if not query:
            raise HTTPException(status_code=404, detail="Запрос не найден или недоступен")

        total = await QueriesDataDAO.get_query_data_count(
            query_id=request_data.query_id,
            keyword_type_category=request_data.keyword_type_category,
            db=db
        )

        if total == 0:
            return QueryDataResponse(
                total=0,
                size=request_data.size,
                total_pages=0
            )

        total_pages = (total + request_data.size - 1) // request_data.size

        if query.query_category != 'name':
            result = QueryDataResponse(
                total=total,
                size=request_data.size,
                total_pages=total_pages
            )
        else:
            fullname_count = await QueriesDataDAO.get_fullname_count(
                query.query_id,
                request_data.keyword_type_category,
                db,
            )
            result = NameQueryDataResponse(
                total=total,
                fullname_count=fullname_count,
                size=request_data.size,
                total_pages=total_pages
            )
        return result
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}, статус: {e.status_code}")
        raise e
    except MissingTokenError:
        logger.error('Неавторизованный пользователь')
        raise HTTPException(status_code=401, detail="Неавторизованный пользователь")
    except Exception as e:
        logger.error(f"Ошибка при получении данных запроса {request_data.query_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Произошла ошибка при получении данных запроса",
        )


@router.get("/general_query_data", response_model=GenerarQueryDataResponse)
async def get_general_query_data(
    query_id: int = Query(..., description="ID запроса"),
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Получает общие данные о выполненном запросе."""
    try:
        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())

        query = await UserQueriesDAO.get_query_by_id(user_id, query_id, db)
        if not query:
            raise HTTPException(status_code=404, detail="Запрос не найден или недоступен")

        languages = await QueryTranslationLanguagesDAO.get_query_languages(query_id, db)
        categories = await QuerySearchCategoryDAO.get_query_categories(query_id, db)
        plus_words = await AdditionalQueryWordDAO.get_query_words_by_type(query_id, "plus", db)
        minus_words = await AdditionalQueryWordDAO.get_query_words_by_type(query_id, "minus", db)
        keyword_stats = await QueryKeywordStatsDAO.get_keyword_stats(query_id, db)

        free_words = []
        if "free word" in keyword_stats:
            free_words = await AdditionalQueryWordDAO.get_query_words_by_type(query_id, "free word", db)

        return GenerarQueryDataResponse(
            query_id=query.query_id,
            query_title=query.query_title,
            languages=languages,
            categories=categories,
            plus_words=plus_words,
            minus_words=minus_words,
            keyword_stats=keyword_stats,
            free_words=free_words,
        )
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}, статус: {e.status_code}")
        raise e
    except MissingTokenError:
        logger.error('Неавторизованный пользователь')
        raise HTTPException(status_code=401, detail="Неавторизованный пользователь")
    except Exception as e:
        logger.error(f"Ошибка при получении данных запроса {query_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Произошла ошибка при получении данных запроса",
        )
