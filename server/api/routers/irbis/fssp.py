from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from server.api.database.database import get_db
from server.api.schemas.irbis.fssp import (
    FSSPDataRequest,
    FSSPCaseFull,
    FSSPDataCase,
)
from server.api.dao.irbis.irbis_person import IrbisPersonDAO
from server.api.dao.irbis.fssp import FSSPDAO
from server.api.utils.route_handler import handle_route_errors
from loguru import logger


router = APIRouter(prefix="/fssp", tags=["Irbis/FSSP"])


@router.post("/data", response_model=List[FSSPDataCase])
@handle_route_errors("Неожиданная ошибка при получении данных ФССП")
async def get_query_data(
    request_data: FSSPDataRequest = Body(...),
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Получает список дел ФССП по выполненному запросу (пагинация)."""
    logger.info(
        f"Запрос fssp_data для query_id: {request_data.query_id}, "
        f"page: {request_data.page}, size: {request_data.size}"
    )
    Authorize.jwt_required()
    user_id = int(Authorize.get_jwt_subject())
    logger.debug(f"Аутентифицированный пользователь: {user_id}")

    irbis_person = await IrbisPersonDAO.get_irbis_person(user_id, request_data.query_id, db)
    if not irbis_person:
        logger.warning(f"Запрос не найден для пользователя {user_id}, query_id: {request_data.query_id}")
        raise HTTPException(status_code=404, detail="Запрос не найден или недоступен")

    results = await FSSPDAO.get_paginated_data(
        irbis_person_id=irbis_person.id,
        page=request_data.page,
        size=request_data.size,
        db=db,
    )
    return [
        FSSPDataCase(
            id=case.id,
            fio=case.fio,
            type_ip=case.type_ip,
            summ=case.summ,
            end_cause=case.end_cause,
        )
        for case in results
    ]


@router.get("/case_full/{case_id}", response_model=FSSPCaseFull)
@handle_route_errors("Неожиданная ошибка при получении дела ФССП")
async def get_full_case_info(
    case_id: int,
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Получает полную информацию по fssp делу и проверяет доступ."""
    logger.info(f"Запрос полной информации о fssp деле id={case_id}")
    Authorize.jwt_required()
    user_id = int(Authorize.get_jwt_subject())
    logger.debug(f"Аутентифицированный пользователь: {user_id}")

    case = await FSSPDAO.get_full_case_by_id(case_id, db)
    if not case:
        logger.warning(f"fssp case id={case_id} не найден")
        raise HTTPException(status_code=404, detail="Дело не найдено")

    owner_id = None
    try:
        owner_id = case.irbis_person.query.user_id
    except Exception:
        owner_id = None

    if owner_id is not None and owner_id != user_id:
        logger.warning(f"Попытка доступа к делу {case_id} пользователем {user_id}. Владелец: {owner_id}")
        raise HTTPException(status_code=403, detail="Доступ запрещен")

    return FSSPCaseFull(
        id=case.id,
        ip=case.ip,
        fio=case.fio,
        rosp=case.rosp,
        type_ip=case.type_ip,
        summ=case.summ,
        rekv=case.rekv,
        end_cause=case.end_cause,
        pristav=case.pristav,
        pristav_phones=case.pristav_phones,
    )
