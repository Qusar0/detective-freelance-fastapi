from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import MissingTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from server.api.database.database import get_db
from server.api.schemas.irbis.irbis_general import RoleTypeInfo
from server.api.schemas.irbis.arbitration_court import (
    ArbitrationCourtDataRequest,
    ArbitrationCourtCase,
    CaseTypeInfo,
    ArbitrationCourtCaseFull,
)
from server.api.dao.irbis.irbis_person import IrbisPersonDAO
from server.api.dao.irbis.arbitration_court import ArbitrationCourtDAO
from loguru import logger


router = APIRouter(prefix="/arbitration_court", tags=["Irbis/Арбитражные суды"])


@router.post("/data", response_model=List[ArbitrationCourtCase])
async def get_query_data(
    request_data: ArbitrationCourtDataRequest = Body(...),
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Получает данные о делах общий юрисдикции по выполненному запросу."""
    try:
        logger.info(
            f"Запрос arbitration_court_data для query_id: {request_data.query_id}, "
            f"page: {request_data.page}, size: {request_data.size}, "
            f"search_type: {request_data.search_type}, "
            f"role: {request_data.role}"
        )

        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())
        logger.debug(f"Аутентифицированный пользователь: {user_id}")

        irbis_person = await IrbisPersonDAO.get_irbis_person(user_id, request_data.query_id, db)
        if not irbis_person:
            logger.warning(f"Запрос не найден для пользователя {user_id}, query_id: {request_data.query_id}")
            raise HTTPException(status_code=404, detail="Запрос не найден или недоступен")

        logger.debug(f"Найден irbis_person: {irbis_person.id}")

        results = await ArbitrationCourtDAO.get_paginated_data(
            irbis_person_id=irbis_person.id,
            page=request_data.page,
            size=request_data.size,
            search_type=request_data.search_type,
            role=request_data.role,
            db=db,
        )
        cases = [
            ArbitrationCourtCase(
                id=case.id,
                court_name=case.court_name_val,
                case_date=case.case_date,
                name=case.name,
                case_number=case.case_number,
                address=case.address_val,
                search_type=case.search_type,
                inn=case.inn,
                case_type=CaseTypeInfo(
                    id=case.case_type.id,
                    name=case.case_type.name,
                ) if case.case_type else None,
                role=RoleTypeInfo(
                    id=case.role.id,
                    name=case.role.russian_name,
                )
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
        logger.error(f"Неожиданная ошибка в: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.get("/case_full/{case_id}", response_model=ArbitrationCourtCaseFull)
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

        case = await ArbitrationCourtDAO.get_full_case_by_id(case_id, db)
        if not case:
            logger.warning(f"Дело {case_id} не найдено")
            raise HTTPException(status_code=404, detail="Дело не найдено")

        if case.irbis_person.query.user_id != user_id:
            logger.warning(
                f"Попытка доступа к делу {case_id} пользователем {user_id}. "
                f"Владелец запроса: {case.irbis_person.query.user_id}"
            )
            raise HTTPException(status_code=403, detail="Доступ запрещен")

        case_full = ArbitrationCourtCaseFull(
            id=case.id,
            court_name=case.court_name_val,
            case_date=case.case_date,
            name=case.name,
            case_number=case.case_number,
            address=case.address_val,
            inn=case.inn,
            case_type=case.case_type.name,
            role=case.role.russian_name,
            region=case.region.name if case.region else None,
            opponents=[opponent.name for opponent in case.oponents],
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
