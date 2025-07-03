import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import PlainTextResponse
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from datetime import datetime, timezone
from typing import Any, Dict, List
from server.api.scripts.sse_manager import generate_sse_message_type
from server.api.services.price import calculate_email_price, calculate_name_price, calculate_num_price
from server.bots.notification_bot import BalanceNotifier
from server.api.database.database import get_db
from server.api.models.models import QueriesData, UserQueries, Events, TextData, QueriesBalance, Language
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
)

from server.api.dao.queries_balance import QueriesBalanceDAO
from server.api.dao.user_queries import UserQueriesDAO
from server.api.dao.user_balances import UserBalancesDAO
from server.api.dao.balance_history import BalanceHistoryDAO
from server.api.services.file_storage import FileStorageService
from server.api.services.text import translate_name_fields, translate_company_fields
from server.tasks.search.company import start_search_by_company
from server.tasks.search.email import start_search_by_email
from server.tasks.search.name import start_search_by_name
from server.tasks.search.number import start_search_by_num

router = APIRouter(
    prefix="/queries",
    tags=["queries"]
)


@router.post("/delete_query")
async def delete_query(
    query_id: int = Query(..., description="ID запроса для удаления"),
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
    file_storage: FileStorageService = Depends(),
):
    try:
        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())

        text_data_result = await db.execute(
            select(TextData)
            .where(TextData.query_id == query_id)
        )
        text_data = text_data_result.scalar_one_or_none()

        if text_data and text_data.file_path:
            await file_storage.delete_query_data(text_data.file_path)

        result = await db.execute(
            select(UserQueries)
            .where(
                UserQueries.query_id == query_id,
                UserQueries.user_id == user_id,
            )
        )
        user_query = result.scalar_one_or_none()

        if not user_query:
            raise HTTPException(status_code=404, detail=f"Query {query_id} not found or doesn't belong to user")

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
    except Exception as e:
        await db.rollback()
        logging.error(f"Delete error for query {query_id}: {str(e)}")
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
            select(UserQueries).where(UserQueries.user_id == user_id, UserQueries.query_category == query_category)
        )
        count = len(result.fetchall())
        return {"count": count}
    except Exception as e:
        logging.error(f"Failed to count queries: {e}")
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

        user_queries = await UserQueriesDAO.get_queries_page([user_id, query_category], page, db=db)

        result_list = []
        query_ids = [str(q.query_id) for q in user_queries]

        for q in user_queries:
            result_list.append({
                "query_id": q.query_id,
                "user_id": q.user_id,
                "query_title": q.query_title,
                "query_unix_date": q.query_unix_date.strftime('%Y/%m/%d %H:%M:%S'),
                "query_created_at": q.query_created_at.strftime('%Y/%m/%d %H:%M:%S'),
                "query_status": q.query_status
            })

        query_ids = [int(qid) for qid in query_ids]

        balances_result = await db.execute(
            select(QueriesBalance)
            .where(QueriesBalance.query_id.in_(query_ids))
        )

        balances = balances_result.scalars().all()
        balance_map = {row.query_id: float(row.balance) for row in balances}

        for item in result_list:
            item["balance"] = balance_map.get(int(item["query_id"]), 0)

        return result_list
    except Exception as e:
        logging.error(f"Failed to get query data: {e}")
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

        query_created_at = datetime.strptime('1980/01/01 00:00:00', '%Y/%m/%d %H:%M:%S')

        query_title = f"{original_data['surname']} {original_data['name']} {original_data['patronymic']}"
        user_query = UserQueries(
            user_id=user_id,
            query_unix_date=query_created_at,
            query_created_at=datetime.now(),
            query_title=query_title,
            query_status="pending",
            query_category="name"
        )

        db.add(user_query)
        await db.commit()

        search_filters = (
            translated_data["name"],
            translated_data["surname"],
            translated_data["patronymic"],
            translated_data["plus"],
            translated_data["minus"],
            translated_data["keywords"],
            default_keywords_type,
            user_query.query_id,
            price,
            search_engines,
            languages
        )

        await UserBalancesDAO.subtract_balance(user_id, price, channel, db)

        await BalanceHistoryDAO.save_payment_to_history(
            price,
            user_query.query_id,
            db,
        )
        await QueriesBalanceDAO.save_query_balance(
            user_query.query_id,
            price,
            db,
        )

        start_search_by_name.apply_async(args=(search_filters,), queue='name_tasks')
        return None
    except Exception as e:
        logging.error(f"Failed to process the query: {e}")
        raise HTTPException(status_code=422, detail="Invalid input")


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

        query_created_at = datetime.strptime('1980/01/01 00:00:00', '%Y/%m/%d %H:%M:%S')

        query_title = search_number
        user_query = UserQueries(
            user_id=user_id,
            query_unix_date=query_created_at,
            query_created_at=datetime.now(),
            query_title=query_title,
            query_status="pending",
            query_category="number"
        )

        db.add(user_query)
        await db.commit()
        await db.refresh(user_query)

        await UserBalancesDAO.subtract_balance(user_id, price, channel, db)

        await BalanceHistoryDAO.save_payment_to_history(
            price,
            user_query.query_id,
            db,
        )
        await QueriesBalanceDAO.save_query_balance(
            user_query.query_id,
            price,
            db,
        )

        start_search_by_num.apply_async(
            args=(search_number, methods_type, user_query.query_id, price),
            queue='num_tasks'
        )
        return None

    except Exception as e:
        logging.error(f"Failed to process the query: {e}")
        raise HTTPException(status_code=422, detail="Invalid input")


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

        query_created_at = datetime.strptime('1980/01/01 00:00:00', '%Y/%m/%d %H:%M:%S')

        query_title = search_email
        user_query = UserQueries(
            user_id=user_id,
            query_unix_date=query_created_at,
            query_created_at=datetime.now(),
            query_title=query_title,
            query_status="pending",
            query_category="email"
        )

        db.add(user_query)
        await db.commit()

        await UserBalancesDAO.subtract_balance(user_id, price, channel, db)

        await BalanceHistoryDAO.save_payment_to_history(
            price,
            user_query.query_id,
            db,
        )
        await QueriesBalanceDAO.save_query_balance(
            user_query.query_id,
            price,
            db,
        )

        start_search_by_email.apply_async(
            args=(search_email, methods_type, user_query.query_id, price),
            queue='email_tasks'
        )
        return None

    except Exception as e:
        logging.error(f"Failed to process the query: {e}")
        raise HTTPException(status_code=422, detail="Invalid input")


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
        query_created_at = datetime.strptime('1980/01/01 00:00:00', '%Y/%m/%d %H:%M:%S')

        query_title = original_data['company_name']
        user_query = UserQueries(
            user_id=user_id,
            query_unix_date=query_created_at,
            query_created_at=datetime.now(),
            query_title=query_title,
            query_status="pending",
            query_category="company"
        )

        db.add(user_query)
        await db.commit()

        search_filters = (
            original_data['company_name'],
            original_data['extra_name'],
            translated_data['location'],
            translated_data['keywords'],
            default_keywords_type,
            translated_data['plus'],
            translated_data['minus'],
            user_query.query_id,
            price,
            search_engines,
            languages
        )

        await UserBalancesDAO.subtract_balance(user_id, price, channel, db)

        await BalanceHistoryDAO.save_payment_to_history(
            price,
            user_query.query_id,
            db,
        )
        await QueriesBalanceDAO.save_query_balance(
            user_query.query_id,
            price,
            db,
        )

        start_search_by_company.apply_async(args=(search_filters,), queue='company_tasks')
        return None
    except Exception as e:
        logging.error(f"Failed to process the query: {e}")
        raise HTTPException(status_code=422, detail="Invalid input")


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
    except Exception as e:
        logging.warning(f"Invalid input: {e}")
        raise HTTPException(status_code=422, detail="Invalid input")


@router.post("/download_query", response_class=PlainTextResponse)
async def download_query(
    data: DownloadQueryRequest,
    db: AsyncSession = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    file_storage: FileStorageService = Depends(),
):
    try:
        Authorize.jwt_required()
    except Exception as e:
        logging.warning(f"JWT auth failed: {e}")
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        query_id = data.query_id

        query_result = await db.execute(
            select(UserQueries).where(UserQueries.query_id == query_id)
        )
        query_record = query_result.scalar_one_or_none()
        if query_record is None:
            raise HTTPException(status_code=404, detail="This user hasn't such a query")

        if query_record.query_unix_date == datetime(1980, 1, 1, tzinfo=timezone.utc):
            await db.execute(
                update(UserQueries)
                .where(UserQueries.query_id == query_id)
                .values(
                    query_unix_date=datetime.now(
                        timezone.utc
                    ),
                ),
            )
            await db.commit()

        text_result = await db.execute(
            select(TextData.file_path).where(TextData.query_id == query_id)
        )
        file_path = text_result.scalar_one_or_none()

        if not file_path:
            raise HTTPException(status_code=404, detail="Query data not found")

        query_text = await file_storage.get_query_data(file_path)

        return PlainTextResponse(content=query_text, media_type='text/plain; charset=UTF-8')

    except Exception as e:
        logging.error(f"Download query failed: {e}")
        raise HTTPException(status_code=422, detail="Invalid input")


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
    except Exception as e:
        logging.error(f"Не удалось получить языки: {e}")
        raise HTTPException(status_code=500, detail="Ошибка получения языков")


@router.get("/query_data", response_model=List[Dict[str, Any]])
async def get_query_data(
    query_id: int = Query(..., description="ID запроса"),
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """
    Получает данные о выполненном запросе в формате:
    """
    try:
        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())

        query_exists = await db.execute(
            select(UserQueries)
            .where(
                UserQueries.query_id == query_id,
                UserQueries.user_id == user_id
            )
        )
        if not query_exists.scalar():
            raise HTTPException(status_code=404, detail="Запрос не найден или недоступен")

        data_result = await db.execute(
            select(QueriesData)
            .where(QueriesData.query_id == query_id)
            .order_by(QueriesData.created_at.desc())
        )
        query_data = data_result.scalars().first()

        if not query_data:
            raise HTTPException(status_code=404, detail="Данные запроса не найдены")

        results = []

        if isinstance(query_data.found_info, str):
            infos = [info.strip() for info in query_data.found_info.split('\n') if info.strip()]
            links = query_data.found_links or []

            for i, info in enumerate(infos):
                result = {"info": info}
                if i < len(links):
                    result["url"] = links[i]
                results.append(result)

        elif query_data.found_links:
            results = [{"url": link} for link in query_data.found_links]

        return results

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Ошибка при получении данных запроса {query_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Произошла ошибка при получении данных запроса"
        )
