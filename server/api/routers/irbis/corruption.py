from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from server.api.database.database import get_db
from server.api.schemas.irbis.corruption import (
    CorruptionDataRequest,
    CorruptionCaseFull,
    CorruptionDataCase,
)
from server.api.dao.irbis.irbis_person import IrbisPersonDAO
from server.api.dao.irbis.corruption import CorruptionDAO
from server.api.utils.route_handler import handle_route_errors
from loguru import logger


router = APIRouter(prefix="/corruption", tags=["Irbis/Коррупция"])


@router.post("/data", response_model=List[CorruptionDataCase])
@handle_route_errors("Неожиданная ошибка при получении данных коррупции")
async def get_query_data(
    request_data: CorruptionDataRequest = Body(...),
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Получает список дел коррупции по выполненному запросу (пагинация)."""
    logger.info(
        f"Запрос corruption_data для query_id: {request_data.query_id}, "
        f"page: {request_data.page}, size: {request_data.size}"
    )
    Authorize.jwt_required()
    user_id = int(Authorize.get_jwt_subject())
    logger.debug(f"Аутентифицированный пользователь: {user_id}")

    irbis_person = await IrbisPersonDAO.get_irbis_person(user_id, request_data.query_id, db)
    if not irbis_person:
        logger.warning(f"Запрос не найден для пользователя {user_id}, query_id: {request_data.query_id}")
        raise HTTPException(status_code=404, detail="Запрос не найден или недоступен")

    results = await CorruptionDAO.get_paginated_data(
        irbis_person_id=irbis_person.id,
        page=request_data.page,
        size=request_data.size,
        db=db,
    )
    return [
        CorruptionDataCase(
            id=case.id,
            full_name=case.full_name,
            organization=case.organization,
            position=case.position,
            application_date=case.application_date,
        )
        for case in results
    ]


@router.get("/case_full/{case_id}", response_model=CorruptionCaseFull)
@handle_route_errors("Неожиданная ошибка при получении дела коррупции")
async def get_full_case_info(
    case_id: int,
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Получает полную информацию по corruption делу и проверяет доступ."""
    logger.info(f"Запрос полной информации о corruption деле id={case_id}")
    Authorize.jwt_required()
    user_id = int(Authorize.get_jwt_subject())
    logger.debug(f"Аутентифицированный пользователь: {user_id}")

    case = await CorruptionDAO.get_full_case_by_id(case_id, db)
    if not case:
        logger.warning(f"corruption case id={case_id} не найден")
        raise HTTPException(status_code=404, detail="Дело не найдено")

    owner_id = None
    try:
        owner_id = case.irbis_person.query.user_id
    except Exception:
        owner_id = None

    if owner_id is not None and owner_id != user_id:
        logger.warning(f"Попытка доступа к делу {case_id} пользователем {user_id}. Владелец: {owner_id}")
        raise HTTPException(status_code=403, detail="Доступ запрещен")

    return CorruptionCaseFull(
        id=case.id,
        full_name=case.full_name,
        organization=case.organization,
        position=case.position,
        normative_act=case.normative_act,
        application_date=case.application_date,
        publish_date=case.publish_date,
        excluded_reason=case.excluded_reason,
    )
