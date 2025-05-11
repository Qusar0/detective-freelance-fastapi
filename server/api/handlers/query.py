from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import PlainTextResponse
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
from datetime import datetime, timezone
from typing import List

from server.api.database.database import get_db
from server.api.models.models import UserQueries, Events, TextData, QueriesBalance
from server.api.schemas.query import (
    QueriesCountResponse,
    QueryData,
    FindByNameModel,
    SearchResponseModel,
    FindByNumberModel,
    FindByEmailModel,
    FindByCompanyModel,
    CalculatePriceRequest,
    PriceResponse,
    DownloadQueryRequest,
)
from server.celery_tasks import (
    start_search_by_name,
    start_search_by_num,
    start_search_by_email,
    start_search_by_company,
    start_search_by_telegram,
)
from server.api.scripts import utils
from server.api.scripts import db_transactions
import logging


router = APIRouter(
    prefix="/queries",
    tags=["queries"]
)


@router.post("/delete_query")
async def delete_query(
    query_id: int = Query(..., description="ID запроса для удаления"),
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    try:
        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())

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

        user_queries = await utils.get_queries_page([user_id, query_category], page, db=db)

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
async def find_by_name(
    request_data: FindByNameModel,
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    try:
        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())

        search_name = request_data.search_name.strip()
        search_surname = request_data.search_surname.strip()
        search_patronymic = request_data.search_patronymic.strip()
        search_plus = request_data.search_plus.strip()
        search_minus = request_data.search_minus.strip()
        keywords: List[str] = request_data.keywords
        default_keywords_type = request_data.default_keywords_type.strip()
        use_yandex = request_data.use_yandex
        languages = request_data.languages

        channel = await utils.generate_sse_message_type(user_id=user_id, db=db)

        price = await utils.calculate_name_price(
            db,
            search_patronymic,
            keywords,
            default_keywords_type,
        )

        query_created_at = datetime.strptime('1980/01/01 00:00:00', '%Y/%m/%d %H:%M:%S')

        query_title = f"{search_surname} {search_name} {search_patronymic}"
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
            search_name,
            search_surname,
            search_patronymic,
            search_plus,
            search_minus,
            keywords,
            default_keywords_type,
            user_query.query_id,
            price,
            use_yandex,
            # languages
        )

        await utils.subtract_balance(user_id, price, channel, db)

        await db_transactions.save_payment_to_history(
            user_id,
            price,
            user_query.query_id,
            db,
        )
        await db_transactions.save_query_balance(
            user_query.query_id,
            price,
            db,
        )

        start_search_by_name.apply_async(args=[search_filters], queue='name_tasks')

    except Exception as e:
        logging.error(f"Failed to process the query: {e}")
        raise HTTPException(status_code=422, detail="Invalid input")


@router.post("/find_by_number")
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
        use_yandex = request_data.use_yandex
        languages = request_data.languages

        channel = await utils.generate_sse_message_type(user_id=user_id, db=db)
        price = utils.calculate_num_price(methods_type)

        query_created_at = datetime.strptime('1980/01/01 00:00:00', '%Y/%m/%d %H:%M:%S')

        user_query = UserQueries(
            user_id=user_id,
            query_unix_date=query_created_at,
            query_created_at=datetime.now(),
            query_title=search_number,
            query_status="pending",
            query_category="number"
        )

        db.add(user_query)
        await db.commit()
        await db.refresh(user_query)

        await utils.subtract_balance(user_id, price, channel, db)
        await db_transactions.save_payment_to_history(user_id, price, user_query.query_id, db)
        await db_transactions.save_query_balance(user_query.query_id, price, db)

        search_filters = (
            search_number,
            methods_type,
            user_query.query_id,
            use_yandex,
            # languages
        )

        start_search_by_num.apply_async((search_filters), queue='num_tasks')

    except Exception as e:
        logging.error(f"Failed to process the phone number query: {e}")
        raise HTTPException(status_code=422, detail="Invalid input")


@router.post("/find_by_email")
async def find_by_email(
    request_data: FindByEmailModel,
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    try:
        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())

        email = request_data.email.strip()
        methods_type = request_data.methods_type
        use_yandex = request_data.use_yandex
        languages = request_data.languages

        channel = await utils.generate_sse_message_type(user_id=user_id, db=db)
        price = utils.calculate_email_price(methods_type)

        query_created_at = datetime.strptime('1980/01/01 00:00:00', '%Y/%m/%d %H:%M:%S')

        user_query = UserQueries(
            user_id=user_id,
            query_unix_date=query_created_at,
            query_created_at=datetime.now(),
            query_title=email,
            query_status="pending",
            query_category="email"
        )

        db.add(user_query)
        await db.commit()
        await db.refresh(user_query)

        await utils.subtract_balance(user_id, price, channel, db)
        await db_transactions.save_payment_to_history(
            user_id,
            price,
            user_query.query_id,
            db,
        )
        await db_transactions.save_query_balance(
            user_query.query_id,
            price,
            db,
        )

        search_filters = (
            email,
            methods_type,
            user_query.query_id,
            use_yandex,
            # languages
        )

        start_search_by_email.apply_async(
            (search_filters),
            queue='email_tasks',
        )

    except Exception as e:
        logging.error(f"Failed to process the email query: {e}")
        raise HTTPException(status_code=422, detail="Invalid input")


@router.post("/find_by_company")
async def find_by_company(
    request_data: FindByCompanyModel,
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    try:
        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())

        company_name = request_data.company_name.strip()
        extra_name = request_data.extra_name.strip()
        location = request_data.location.strip()
        keywords = request_data.keywords
        default_keywords_type = request_data.default_keywords_type.strip()
        plus_words = request_data.search_plus.strip()
        minus_words = request_data.search_minus.strip()
        use_yandex = request_data.use_yandex
        languages = request_data.languages

        channel = await utils.generate_sse_message_type(user_id=user_id, db=db)
        price = 10

        query_created_at = datetime.strptime('1980/01/01 00:00:00', '%Y/%m/%d %H:%M:%S')

        user_query = UserQueries(
            user_id=user_id,
            query_unix_date=query_created_at,
            query_created_at=datetime.now(),
            query_title=company_name,
            query_status="pending",
            query_category="company",
        )

        db.add(user_query)
        await db.commit()
        await db.refresh(user_query)

        await utils.subtract_balance(user_id, price, channel, db)
        await db_transactions.save_payment_to_history(
            user_id,
            price,
            user_query.query_id,
            db,
        )
        await db_transactions.save_query_balance(
            user_query.query_id,
            price,
            db,
        )

        search_filters = (
            company_name,
            extra_name,
            location,
            keywords,
            default_keywords_type,
            plus_words,
            minus_words,
            user_query.query_id,
            price,
            use_yandex,
            # languages
        )

        start_search_by_company.apply_async(
            (search_filters,),
            queue="company_tasks",
        )

    except Exception as e:
        logging.error(f"Failed to process the company query: {e}")
        raise HTTPException(status_code=422, detail="Invalid input")


@router.post("/calculate_price", response_model=PriceResponse)
async def calculate_price(
    data: CalculatePriceRequest,
    db: AsyncSession = Depends(get_db),
    Authorize: AuthJWT = Depends(),
):
    try:
        Authorize.jwt_required()
        price = await utils.calculate_name_price(
            db,
            data.search_patronymic.strip(),
            data.keywords,
            data.default_keywords_type.strip(),
        )
        return {"price": price}
    except Exception as e:
        logging.warning(f"Invalid input: {e}")
        raise HTTPException(status_code=422, detail="Invalid input")


@router.post("/download_query", response_class=PlainTextResponse)
async def download_query(
    data: DownloadQueryRequest,
    db: AsyncSession = Depends(get_db),
    Authorize: AuthJWT = Depends()
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
            select(TextData.query_data).where(TextData.query_id == query_id)
        )
        query_text = text_result.scalar_one_or_none()

        if not query_text:
            raise HTTPException(status_code=404, detail="Query data not found")

        return PlainTextResponse(content=query_text, media_type='text/plain; charset=UTF-8')

    except Exception as e:
        logging.error(f"Download query failed: {e}")
        raise HTTPException(status_code=422, detail="Invalid input")