from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import MissingTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from server.api.database.database import get_db

from server.api.schemas.irbis.bankruptcy import (
    BankruptcyDataRequest,
    BankruptcyCaseFull,
    BankruptcyDataCase,
    BankruptcyDataResponse,
)
from server.api.dao.irbis.irbis_person import IrbisPersonDAO
from server.api.dao.irbis.bankruptcy import BankruptcyDAO
from loguru import logger


router = APIRouter(prefix="/bankruptcy", tags=["Irbis/Банкротства"])


@router.post("/data", response_model=BankruptcyDataResponse)
async def get_query_data(
    request_data: BankruptcyDataRequest = Body(...),
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Получает данные о ,банкротствах по выполненному запросу."""
    try:
        logger.info(
            f"Запрос bankruptcy_data для query_id: {request_data.query_id}, "
            f"page: {request_data.page}, size: {request_data.size}, "
            f"search_type: {request_data.search_type}, "
        )

        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())
        logger.debug(f"Аутентифицированный пользователь: {user_id}")

        irbis_person = await IrbisPersonDAO.get_irbis_person(user_id, request_data.query_id, db)
        if not irbis_person:
            logger.warning(f"Запрос не найден для пользователя {user_id}, query_id: {request_data.query_id}")
            raise HTTPException(status_code=404, detail="Запрос не найден или недоступен")

        logger.debug(f"Найден irbis_person: {irbis_person.id}")

        results, total_count = await BankruptcyDAO.get_paginated_data(
            irbis_person_id=irbis_person.id,
            page=request_data.page,
            size=request_data.size,
            search_type=request_data.search_type,
            db=db,
        )

        cases = [
            BankruptcyDataCase(
                id=case.id,
                first_name=case.first_name,
                second_name=case.second_name,
                last_name=case.last_name,
                category_name=case.category_name,
                birth_date=case.birth_date,
                born_place=case.born_place,
                region_name=case.region_name
            )
            for case in results
        ]

        total_pages = (total_count + request_data.size - 1) // request_data.size if request_data.size > 0 else 0

        return BankruptcyDataResponse(
            cases=cases,
            total_count=total_count,
            total_pages=total_pages
        )

    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}, статус: {e.status_code}")
        raise e
    except MissingTokenError:
        logger.error('Неавторизованный пользователь')
        raise HTTPException(status_code=401, detail="Неавторизованный пользователь")
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.get("/case_full/{case_id}", response_model=BankruptcyCaseFull)
async def get_full_case_info(
    case_id: int,
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Получает полную информацию о банкротсвах по ID."""
    try:
        logger.info(f"Запрос полной информации по делу ID: {case_id}")

        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())
        logger.debug(f"Аутентифицированный пользователь: {user_id}")

        case = await BankruptcyDAO.get_full_case_by_id(case_id, db)
        if not case:
            logger.warning(f"Дело {case_id} не найдено")
            raise HTTPException(status_code=404, detail="Дело не найдено")

        if case.irbis_person.query.user_id != user_id:
            logger.warning(
                f"Попытка доступа к делу {case_id} пользователем {user_id}. "
                f"Владелец запроса: {case.irbis_person.query.user_id}"
            )
            raise HTTPException(status_code=403, detail="Доступ запрещен")

        case_full = BankruptcyCaseFull(
            id=case.id,
            first_name=case.first_name,
            second_name=case.second_name,
            last_name=case.last_name,
            birth_date=case.birth_date,
            born_place=case.born_place,
            inn=case.inn,
            ogrn=case.ogrn,
            snils=case.snils,
            old_name=case.old_name,
            category_name=case.category_name,
            location=case.location,
            region_name=case.region_name,
            information=case.information,
            link=case.link
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
        logger.error(f"Неожиданная ошибка в get_full_case_info: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")
