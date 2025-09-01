from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import MissingTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from server.api.database.database import get_db
from server.api.schemas.irbis import (
    CourtGeneralCase,
    RegionInfo,
    ProcessTypeInfo,
    IrbisDataRequest,
    IrbisPersonInfo,
    CourtGeneralCaseFull,
    MatchTypeInfo,
    CourtGeneralFace,
    CourtGeneralProgress,
)
from server.api.dao.irbis.irbis_person import IrbisPersonDAO
from server.api.dao.irbis.court_general_jur import CourtGeneralJurDAO
from server.api.dao.irbis.region_subjects import RegionSubjectDAO
from loguru import logger


router = APIRouter(
    prefix="/irbis",
    tags=["irbis"]
)


@router.post("/court_general_data", response_model=Optional[List[CourtGeneralCase]])
async def get_query_data(
    request_data: IrbisDataRequest = Body(...),
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

        results = await CourtGeneralJurDAO.get_paginated_court_general_data(
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
                    code=case.region.subject_number,
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
        logger.error(f"HTTPException в court_general_data: {e.detail}, статус: {e.status_code}")
        raise e
    except MissingTokenError:
        logger.error('Неавторизованный пользователь')
        raise HTTPException(status_code=401, detail="Неавторизованный пользователь")
    except Exception as e:
        logger.error(f"Неожиданная ошибка в court_general_data: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.get("/person_info/{query_id}", response_model=IrbisPersonInfo)
async def get_person_info(
    query_id: int,
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Получает общую информацию о человеке по ID запроса."""
    try:
        logger.info(f"Запрос информации о человеке для query_id: {query_id}")

        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())
        logger.debug(f"Аутентифицированный пользователь: {user_id}")

        irbis_person = await IrbisPersonDAO.get_irbis_person(user_id, query_id, db)
        if not irbis_person:
            logger.warning(f"Запрос не найден для пользователя {user_id}, query_id: {query_id}")
            raise HTTPException(status_code=404, detail="Запрос не найден или недоступен")

        regions = await RegionSubjectDAO.get_person_regions(irbis_person.id, db)
        logger.debug(f"Получено {len(regions)} регионов для person_id: {irbis_person.id}")

        person_info = IrbisPersonInfo(
            fullname=irbis_person.fullname,
            birth_date=irbis_person.birth_date,
            passport_series=irbis_person.passport_series,
            passport_number=irbis_person.passport_number,
            inn=irbis_person.inn,
            regions=[
                RegionInfo(
                    code=region.subject_number,
                    name=region.name
                )
                for region in regions
            ]
        )

        logger.success(f"Успешно возвращена информация о человеке: {irbis_person.fullname}")
        return person_info

    except HTTPException as e:
        logger.warning(f"HTTPException в get_person_info: {e.detail}, статус: {e.status_code}")
        raise e
    except MissingTokenError:
        logger.error('Неавторизованный пользователь')
        raise HTTPException(status_code=401, detail="Неавторизованный пользователь")
    except Exception as e:
        logger.error(f"Неожиданная ошибка в get_person_info: {e}", exc_info=True)
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
                code=case.region.subject_number,
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
        logger.warning(f"HTTPException в get_full_case_info: {e.detail}, статус: {e.status_code}")
        raise e
    except MissingTokenError:
        logger.error('Неавторизованный пользователь')
        raise HTTPException(status_code=401, detail="Неавторизованный пользователь")
    except Exception as e:
        logger.error(f"Неожиданная ошибка в get_full_case_info: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")
