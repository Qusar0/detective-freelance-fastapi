from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import MissingTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from server.api.database.database import get_db

from server.api.schemas.irbis.disqualified_person import (
    DisqDataRequest,
    DisqCaseFull,
    DisqDataCase,
)
from server.api.dao.irbis.irbis_person import IrbisPersonDAO
from server.api.dao.irbis.disqualified_person import DisqualifiedPersonDAO
from loguru import logger


router = APIRouter(prefix="/disqualified_person", tags=["Irbis/Дисквалифицированные лица"])


@router.post("/data", response_model=List[DisqDataCase])
async def get_query_data(
    request_data: DisqDataRequest = Body(...),
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Получает данные о дисквалифицированных лицах по выполненному запросу."""
    try:
        logger.info(
            f"Запрос disqualified_person_data для query_id: {request_data.query_id}, "
            f"page: {request_data.page}, size: {request_data.size}"
        )

        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())
        logger.debug(f"Аутентифицированный пользователь: {user_id}")

        irbis_person = await IrbisPersonDAO.get_irbis_person(user_id, request_data.query_id, db)
        if not irbis_person:
            logger.warning(f"Запрос не найден для пользователя {user_id}, query_id: {request_data.query_id}")
            raise HTTPException(status_code=404, detail="Запрос не найден или недоступен")

        logger.debug(f"Найден irbis_person: {irbis_person.id}")

        results = await DisqualifiedPersonDAO.get_paginated_data(
            irbis_person_id=irbis_person.id,
            page=request_data.page,
            size=request_data.size,
            db=db,
        )
        cases = [
            DisqDataCase(
                id=case.id,
                fio=case.fio,
                start_date_disq=case.start_date_disq,
                end_date_disq=case.end_date_disq,
                article=case.article,
                legal_name=case.legal_name,
                office=case.office,
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
        logger.error(f"Неожиданная ошибка: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.get("/case_full/{case_id}", response_model=DisqCaseFull)
async def get_full_case_info(
    case_id: int,
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Получает полную информацию о банкротсвах по ID."""
    try:
        logger.info(f"Запрос полной информации о дисквалифицированных лицах по ID: {case_id}")

        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())
        logger.debug(f"Аутентифицированный пользователь: {user_id}")

        case = await DisqualifiedPersonDAO.get_full_case_by_id(case_id, db)
        if not case:
            logger.warning(f"Дело {case_id} не найдено")
            raise HTTPException(status_code=404, detail="Дело не найдено")

        if case.irbis_person.query.user_id != user_id:
            logger.warning(
                f"Попытка доступа к делу {case_id} пользователем {user_id}. "
                f"Владелец запроса: {case.irbis_person.query.user_id}"
            )
            raise HTTPException(status_code=403, detail="Доступ запрещен")

        case_full = DisqCaseFull(
            id=case.id,
            birth_date=case.birth_date,
            fio=case.fio,
            article=case.article,
            start_date_disq=case.start_date_disq,
            end_date_disq=case.end_date_disq,
            bornplace=case.bornplace,
            fio_judge=case.fio_judge,
            office_judge=case.office_judge,
            legal_name=case.legal_name,
            office=case.office,
            department=case.department
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
