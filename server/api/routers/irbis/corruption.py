from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import MissingTokenError
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
from loguru import logger


router = APIRouter(prefix="/corruption", tags=["Irbis/Коррупция"])


@router.post("/data", response_model=List[CorruptionDataCase])
async def get_query_data(
    request_data: CorruptionDataRequest = Body(...),
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Получает список дел коррупции по выполненному запросу (пагинация)."""
    try:
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

        logger.debug(f"Найден irbis_person: {irbis_person.id}")

        results = await CorruptionDAO.get_paginated_data(
            irbis_person_id=irbis_person.id,
            page=request_data.page,
            size=request_data.size,
            db=db,
        )

        cases = [
            CorruptionDataCase(
                id=case.id,
                full_name=case.full_name,
                organization=getattr(case, "organization"),
                position=getattr(case, "position"),
                application_date=getattr(case, "application_date"),
            )
            for case in results
        ]
        return cases

    except HTTPException as e:
        logger.warning(f"HTTPException в corruption_data: {e.detail}, статус: {e.status_code}")
        raise e
    except MissingTokenError:
        logger.error("Неавторизованный пользователь")
        raise HTTPException(status_code=401, detail="Неавторизованный пользователь")
    except Exception as e:
        logger.error(f"Неожиданная ошибка в: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.get("/case_full/{case_id}", response_model=CorruptionCaseFull)
async def get_full_case_info(
    case_id: int,
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Получает полную информацию по corruption делу и проверяет доступ."""
    try:
        logger.info(f"Запрос полной информации о corruption деле id={case_id}")

        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())
        logger.debug(f"Аутентифицированный пользователь: {user_id}")

        case = await CorruptionDAO.get_full_case_by_id(case_id, db)
        if not case:
            logger.warning(f"corruption case id={case_id} не найден")
            raise HTTPException(status_code=404, detail="Дело не найдено")

        # Проверка владельца запроса
        owner_id = None
        try:
            owner_id = case.irbis_person.query.user_id
        except Exception:
            owner_id = None

        if owner_id is not None and owner_id != user_id:
            logger.warning(
                f"Попытка доступа к делу {case_id} пользователем {user_id}. Владелец запроса: {owner_id}"
            )
            raise HTTPException(status_code=403, detail="Доступ запрещен")

        # Преобразуем ORM-объект в Pydantic модель
        case_full = CorruptionCaseFull(
            id=case.id,
            full_name=case.full_name,
            organization=getattr(case, "organization", None),
            position=getattr(case, "position", None),
            normative_act=getattr(case, "normative_act", None),
            application_date=getattr(case, "application_date", None),
            publish_date=getattr(case, "publish_date", None),
            excluded_reason=getattr(case, "excluded_reason", None),
        )
        return case_full

    except HTTPException as e:
        logger.warning(f"HTTPException в get_full_case_info: {e.detail}, статус: {e.status_code}")
        raise e
    except MissingTokenError:
        logger.error("Неавторизованный пользователь")
        raise HTTPException(status_code=401, detail="Неавторизованный пользователь")
    except Exception as e:
        logger.error(f"Неожиданная ошибка в get_full_case_info: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")
