from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import MissingTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
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
)
from server.api.dao.irbis.irbis_person import IrbisPersonDAO
from server.api.dao.irbis.court_general_jur import CourtGeneralJurDAO
from server.api.dao.irbis.process_type import ProcessTypeDAO
from loguru import logger


router = APIRouter(prefix="/court_general", tags=["Irbis/Суды общей юрисдикции"])


@router.get('/process_types', response_model=List[ProcessTypeInfo])
async def get_process_types(db: AsyncSession = Depends(get_db)):
    """Получает данные о типах судебных процессов."""
    try:
        process_types = await ProcessTypeDAO.find_all(db)
        return [
            ProcessTypeInfo(
                code=process_type.code,
                name=process_type.name,
            )
            for process_type in process_types
        ]
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}, статус: {e.status_code}")
        raise e
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.post("/data", response_model=Optional[List[CourtGeneralCase]])
async def get_query_data(
    request_data: CourtGeneralDataRequest = Body(...),
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Получает данные о делах общий юрисдикции по выполненному запросу."""
    try:
        logger.info(
            f"Запрос court_general_data для query_id: {request_data.query_id}, "
            f"page: {request_data.page}, size: {request_data.size}, "
            f"all_regions: {request_data.all_regions}, "
            f"categories: {request_data.case_categories}"
        )

        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())
        logger.debug(f"Аутентифицированный пользователь: {user_id}")

        irbis_person = await IrbisPersonDAO.get_irbis_person(user_id, request_data.query_id, db)
        if not irbis_person:
            logger.warning(f"Запрос не найден для пользователя {user_id}, query_id: {request_data.query_id}")
            raise HTTPException(status_code=404, detail="Запрос не найден или недоступен")

        logger.debug(f"Найден irbis_person: {irbis_person.id}")

        results = await CourtGeneralJurDAO.get_paginated_data(
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
                region=RegionInfo(
                    id=case.region.id,
                    name=case.region.name,
                ),
                process_type=ProcessTypeInfo(
                    code=case.process_type.code,
                    name=case.process_type.name,
                ),
                judge=case.judge,
                papers=case.papers,
                papers_pretty=case.papers_pretty,
            )
            for case in results
        ]
        return cases

    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}, статус: {e.status_code}")
        raise e
    except MissingTokenError:
        logger.error('Неавторизованный пользователь')
        raise HTTPException(status_code=401, detail="Неавторизованный пользователь")
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.get("/case_full/{case_id}", response_model=CourtGeneralCaseFull)
async def get_full_case_info(
    case_id: int,
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Получает полную информацию о судебном деле по ID дела."""
    try:
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

        case_full = CourtGeneralCaseFull(
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
            region=RegionInfo(
                id=case.region.id,
                name=case.region.name,
            ),
            process_type=ProcessTypeInfo(
                code=case.process_type.code,
                name=case.process_type.name,
            ),
            match_type=MatchTypeInfo(
                id=case.match_type.id,
                name=case.match_type.name,
            ) if case.match_type else None,
            faces=[
                CourtGeneralFace(
                    role=face.role,
                    face=face.face,
                    role_name=face.role_name,
                )
                for face in case.faces
            ],
            progress=[
                CourtGeneralProgress(
                    name=progress.name,
                    progress_data=progress.progress_date,
                    resolution=progress.resolution,
                )
                for progress in case.progress
            ]
        )

        logger.success(f"Успешно возвращена полная информация по делу {case_id}")
        return case_full

    except HTTPException as e:
        logger.warning(f"HTTPException: {e.detail}, статус: {e.status_code}")
        raise e
    except MissingTokenError:
        logger.error('Неавторизованный пользователь')
        raise HTTPException(status_code=401, detail="Неавторизованный пользователь")
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")
