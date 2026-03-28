from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from server.api.database.database import get_db
from server.api.schemas.irbis.tax_arrears import (
    TaxArrearsDataRequest,
    TaxArrearsDataCase,
    PaymentItemCase
)
from server.api.dao.irbis.irbis_person import IrbisPersonDAO
from server.api.dao.irbis.tax_arrears import TaxArrearsDAO
from server.api.utils.route_handler import handle_route_errors
from loguru import logger


router = APIRouter(prefix="/tax_arrears", tags=["Irbis/Налоговые задолженности"])


@router.post("/data", response_model=List[TaxArrearsDataCase])
@handle_route_errors("Неожиданная ошибка при получении налоговых задолженностей")
async def get_query_data(
    request_data: TaxArrearsDataRequest = Body(...),
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Получает список дел налоговых задолженностей по выполненному запросу (пагинация)."""
    logger.info(
        f"Запрос tax_arrears_data для query_id: {request_data.query_id}, "
        f"page: {request_data.page}, size: {request_data.size}"
    )
    Authorize.jwt_required()
    user_id = int(Authorize.get_jwt_subject())
    logger.debug(f"Аутентифицированный пользователь: {user_id}")

    irbis_person = await IrbisPersonDAO.get_irbis_person(user_id, request_data.query_id, db)
    if not irbis_person:
        logger.warning(f"Запрос не найден для пользователя {user_id}, query_id: {request_data.query_id}")
        raise HTTPException(status_code=404, detail="Запрос не найден или недоступен")

    results = await TaxArrearsDAO.get_paginated_data(
        irbis_person_id=irbis_person.id,
        page=request_data.page,
        size=request_data.size,
        db=db,
    )
    return [
        TaxArrearsDataCase(
            provider=case.provider,
            money_name=case.money_name,
            value=case.money_value,
            info=[f.value for f in case.fields if f.type == 'info'],
            payment=[PaymentItemCase(name=f.field_name, value=f.value) for f in case.fields if f.type == 'payment'],
        )
        for case in results
    ]
