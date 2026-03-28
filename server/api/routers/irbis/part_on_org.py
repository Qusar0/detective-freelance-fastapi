from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from server.api.database.database import get_db
from server.api.schemas.irbis.part_in_org import (
    PartInOrgGeneralCase,
    PartInOrgDataRequest,
    PartInOrgCaseFull,
    OrgObjectSchema,
    IndividualObjectSchema,
    RoleObjectSchema
)
from server.api.dao.irbis.irbis_person import IrbisPersonDAO
from server.api.dao.irbis.part_in_org import PartInOrgDAO
from server.api.utils.route_handler import handle_route_errors
from loguru import logger


router = APIRouter(prefix="/part_in_org", tags=["Irbis/Участие в организациях"])


@router.post("/data", response_model=Optional[List[PartInOrgGeneralCase]])
@handle_route_errors("Неожиданная ошибка при получении данных об участии в организациях")
async def get_query_data(
    request_data: PartInOrgDataRequest = Body(...),
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Получает данные об участии в организациях по выполненному запросу."""
    logger.info(
        f"Запрос part_in_org_data для query_id: {request_data.query_id}, "
        f"page: {request_data.page}, size: {request_data.size}"
    )
    Authorize.jwt_required()
    user_id = int(Authorize.get_jwt_subject())
    logger.debug(f"Аутентифицированный пользователь: {user_id}")

    irbis_person = await IrbisPersonDAO.get_irbis_person(user_id, request_data.query_id, db)
    if not irbis_person:
        logger.warning(f"Запрос не найден для пользователя {user_id}, query_id: {request_data.query_id}")
        raise HTTPException(status_code=404, detail="Запрос не найден или недоступен")

    results = await PartInOrgDAO.get_paginated_data(
        irbis_person_id=irbis_person.id,
        page=request_data.page,
        size=request_data.size,
        db=db,
    )
    return [
        PartInOrgGeneralCase(
            case_id=case.id,
            individual_name=case.individual.name,
            org_name=case.org.name,
            org_okved=case.org.okved
        )
        for case in results
    ]


@router.get("/case_full/{case_id}", response_model=PartInOrgCaseFull)
@handle_route_errors("Неожиданная ошибка при получении дела об участии в организации")
async def get_full_case_info(
    case_id: int,
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Получает полную информацию об участии в организациях по ID дела."""
    logger.info(f"Запрос полной информации по делу ID: {case_id}")
    Authorize.jwt_required()
    user_id = int(Authorize.get_jwt_subject())
    logger.debug(f"Аутентифицированный пользователь: {user_id}")

    case = await PartInOrgDAO.get_full_participation_by_id(case_id, db)
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
    return PartInOrgCaseFull(
        case_id=case.id,
        org=OrgObjectSchema(
            name=case.org.name,
            inn=case.org.inn,
            ogrn=case.org.ogrn,
            address=case.org.address,
            okved=case.org.okved
        ),
        individual=IndividualObjectSchema(
            name=case.individual.name,
            inn=case.individual.inn,
            roles=[RoleObjectSchema(name=role.name, active=role.active) for role in case.individual.roles],
        ),
    )
