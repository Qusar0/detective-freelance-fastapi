from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from server.api.database.database import get_db
from server.api.schemas.irbis.pledgess import (
    PledgessGeneralCase,
    PledgessDataRequest,
    PledgessGeneralPledgees,
    PledgessGeneralPledges,
    PledgeObjectSchema,
    PledgePartiesSchema,
    PledgessCaseFull
)
from server.api.dao.irbis.irbis_person import IrbisPersonDAO
from server.api.dao.irbis.pledgess import PledgessDAO
from server.api.utils.route_handler import handle_route_errors
from loguru import logger


router = APIRouter(prefix="/pledgess", tags=["Irbis/Залоги"])


@router.post("/data", response_model=Optional[List[PledgessGeneralCase]])
@handle_route_errors("Неожиданная ошибка при получении данных залогов")
async def get_query_data(
    request_data: PledgessDataRequest = Body(...),
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Получает данные о залогах по выполненному запросу."""
    logger.info(
        f"Запрос pledgess_data для query_id: {request_data.query_id}, "
        f"page: {request_data.page}, size: {request_data.size}"
    )
    Authorize.jwt_required()
    user_id = int(Authorize.get_jwt_subject())
    logger.debug(f"Аутентифицированный пользователь: {user_id}")

    irbis_person = await IrbisPersonDAO.get_irbis_person(user_id, request_data.query_id, db)
    if not irbis_person:
        logger.warning(f"Запрос не найден для пользователя {user_id}, query_id: {request_data.query_id}")
        raise HTTPException(status_code=404, detail="Запрос не найден или недоступен")

    results = await PledgessDAO.get_paginated_data(
        irbis_person_id=irbis_person.id,
        page=request_data.page,
        size=request_data.size,
        db=db,
    )
    return [
        PledgessGeneralCase(
            case_id=case.id,
            pledge_type=case.pledge_type,
            reg_date=case.reg_date,
            pledgers=[PledgessGeneralPledgees(name=p.name) for p in case.parties if p.type == 'pledgers'],
            pledgees=[PledgessGeneralPledgees(name=p.name) for p in case.parties if p.type == 'pledgees'],
            pledges=[PledgessGeneralPledges(pledge_type=p.pledge_type, pledge_num=p.pledge_num) for p in case.pledges]
        )
        for case in results
    ]


@router.get("/case_full/{case_id}", response_model=PledgessCaseFull)
@handle_route_errors("Неожиданная ошибка при получении дела залога")
async def get_full_case_info(
    case_id: int,
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Получает полную информацию о судебном деле по ID дела."""
    logger.info(f"Запрос полной информации о залогах по делу ID: {case_id}")
    Authorize.jwt_required()
    user_id = int(Authorize.get_jwt_subject())
    logger.debug(f"Аутентифицированный пользователь: {user_id}")

    case = await PledgessDAO.get_full_case_by_id(case_id, db)
    if not case:
        logger.warning(f"Дело {case_id} не найдено")
        raise HTTPException(status_code=404, detail="Дело не найдено")

    if case.irbis_person.query.user_id != user_id:
        logger.warning(
            f"Попытка доступа к делу {case_id} пользователем {user_id}. "
            f"Владелец запроса: {case.irbis_person.query.user_id}"
        )
        raise HTTPException(status_code=403, detail="Доступ запрещен")

    logger.success(f"Успешно возвращена полная информация по делу {case_id}")
    return PledgessCaseFull(
        case_id=case.id,
        reg_date=case.reg_date,
        pledge_reestr_number=case.pledge_reestr_number,
        pledge_type=case.pledge_type,
        pledgers=[
            PledgePartiesSchema(name=p.name, birth_date=p.birth_date, inn=p.inn, ogrn=p.ogrn)
            for p in case.parties if p.type == 'pledgers'
        ],
        pledgees=[
            PledgePartiesSchema(name=p.name, type=p.type, inn=p.inn, ogrn=p.ogrn)
            for p in case.parties if p.type == 'pledgees'
        ],
        pledges=[
            PledgeObjectSchema(id=p.id, pledge_num_name=p.pledge_num_name, pledge_num=p.pledge_num, pledge_type=p.pledge_type)
            for p in case.pledges
        ]
    )
