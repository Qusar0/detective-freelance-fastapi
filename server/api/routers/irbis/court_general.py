from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from server.api.database.database import get_db
from server.api.schemas.irbis.irbis_general import (
    RegionInfo,
    ProcessTypeInfo,
    MatchTypeInfo,
)
from server.api.schemas.irbis.court_general import (
    CourtGeneralCase,
    CourtGeneralDataRequest,
    CourtGeneralCaseFull,
    CourtGeneralFace,
    CourtGeneralProgress,
    CourtGeneralDataResponse,
)
from server.api.dao.irbis.irbis_person import IrbisPersonDAO
from server.api.dao.irbis.court_general_jur import CourtGeneralJurDAO
from server.api.dao.irbis.process_type import ProcessTypeDAO
from server.api.utils.route_handler import handle_route_errors
from loguru import logger


router = APIRouter(prefix="/court_general", tags=["Irbis/Суды общей юрисдикции"])


@router.get('/process_types', response_model=List[ProcessTypeInfo])
@handle_route_errors("Неожиданная ошибка при получении типов процессов")
async def get_process_types(db: AsyncSession = Depends(get_db)):
    """Получает данные о типах судебных процессов."""
    process_types = await ProcessTypeDAO.find_all(db)
    return [ProcessTypeInfo(code=pt.code, name=pt.name) for pt in process_types]


@router.post("/data", response_model=CourtGeneralDataResponse)
@handle_route_errors("Неожиданная ошибка при получении данных судов общей юрисдикции")
async def get_query_data(
    request_data: CourtGeneralDataRequest = Body(...),
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Получает данные о делах общей юрисдикции по выполненному запросу."""
    logger.info(
        f"Запрос court_general_data для query_id: {request_data.query_id}, "
        f"page: {request_data.page}, size: {request_data.size}, "
        f"all_regions: {request_data.all_regions}, categories: {request_data.case_categories}"
    )
    Authorize.jwt_required()
    user_id = int(Authorize.get_jwt_subject())
    logger.debug(f"Аутентифицированный пользователь: {user_id}")

    irbis_person = await IrbisPersonDAO.get_irbis_person(user_id, request_data.query_id, db)
    if not irbis_person:
        logger.warning(f"Запрос не найден для пользователя {user_id}, query_id: {request_data.query_id}")
        raise HTTPException(status_code=404, detail="Запрос не найден или недоступен")

    results, total_count = await CourtGeneralJurDAO.get_paginated_data(
        irbis_person_id=irbis_person.id,
        page=request_data.page,
        size=request_data.size,
        all_regions=request_data.all_regions,
        case_categories=request_data.case_categories,
        db=db,
    )
    cases = [
        CourtGeneralCase(
            case_id=case.id,
            case_number=case.case_number,
            court_name=case.court_name,
            start_date=case.start_date,
            end_date=case.end_date,
            review=case.review,
            region=RegionInfo(id=case.region.id, name=case.region.name),
            process_type=ProcessTypeInfo(code=case.process_type.code, name=case.process_type.name),
            judge=case.judge,
            papers=case.papers,
            papers_pretty=case.papers_pretty,
        )
        for case in results
    ]
    total_pages = (total_count + request_data.size - 1) // request_data.size if request_data.size else 0
    return CourtGeneralDataResponse(cases=cases, total_count=total_count, total_pages=total_pages)


@router.get("/case_full/{case_id}", response_model=CourtGeneralCaseFull)
@handle_route_errors("Неожиданная ошибка при получении дела суда общей юрисдикции")
async def get_full_case_info(
    case_id: int,
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Получает полную информацию о судебном деле по ID дела."""
    logger.info(f"Запрос полной информации по делу ID: {case_id}")
    Authorize.jwt_required()
    user_id = int(Authorize.get_jwt_subject())
    logger.debug(f"Аутентифицированный пользователь: {user_id}")

    case = await CourtGeneralJurDAO.get_full_case_by_id(case_id, db)
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
    return CourtGeneralCaseFull(
        case_id=case.id,
        case_number=case.case_number,
        court_name=case.court_name,
        start_date=case.start_date,
        end_date=case.end_date,
        review=case.review,
        judge=case.judge,
        articles=case.articles,
        papers=case.papers,
        papers_pretty=case.papers_pretty,
        links=case.links,
        region=RegionInfo(id=case.region.id, name=case.region.name),
        process_type=ProcessTypeInfo(code=case.process_type.code, name=case.process_type.name),
        match_type=MatchTypeInfo(id=case.match_type.id, name=case.match_type.name) if case.match_type else None,
        faces=[CourtGeneralFace(role=f.role, face=f.face, role_name=f.role_name) for f in case.faces],
        progress=[
            CourtGeneralProgress(name=p.name, progress_data=p.progress_date, resolution=p.resolution)
            for p in case.progress
        ]
    )
