import logging
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from fastapi.responses import PlainTextResponse
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from datetime import datetime
from typing import List
from server.bots.notification_bot import BalanceNotifier
from server.api.database.database import get_db
from server.api.models.models import (
    UserQueries,
    Events,
    TextData,
    QueriesBalance,
    Language,
)
from server.api.schemas.query import (
    IrbisDataRequest,
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
from server.api.dao.irbis.person_uuid import PersonUuidDAO


router = APIRouter(
    prefix="/irbis",
    tags=["irbis"]
)


@router.post("/court_general_data")
async def get_query_data(
    request_data: IrbisDataRequest = Body(...),
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Получает данные о делах общий юрисдикции по выполненному запросу."""
    try:
        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())

        person_uuid = PersonUuidDAO.get_person_uuid(user_id, request_data.query_id, db)
        if not person_uuid:
            raise HTTPException(status_code=404, detail="Запрос не найден или недоступен")

        query_data = await QueriesDataDAO.get_paginated_query_data(
            query_id=request_data.query_id,
            page=request_data.page,
            size=request_data.size,
            db=db,
        )



    except:
        pass