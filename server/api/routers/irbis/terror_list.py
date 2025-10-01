from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import MissingTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from server.api.database.database import get_db
from server.api.schemas.irbis.terror_list import (
    TerroristsDataRequest,
    TerroristsDataCase,
)
from server.api.dao.irbis.irbis_person import IrbisPersonDAO
from server.api.dao.irbis.terror_list import TerroristsDAO
from loguru import logger


router = APIRouter(prefix="/terrorists", tags=["Irbis/Террористы"])


@router.post("/data", response_model=List[TerroristsDataCase])
async def get_query_data(
    request_data: TerroristsDataRequest = Body(...),
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Получает список дел террористов по выполненному запросу (пагинация)."""
    try:
        logger.info(
            f"Запрос terrorist_data для query_id: {request_data.query_id}, "
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

        results = await TerroristsDAO.get_paginated_data(
            irbis_person_id=irbis_person.id,
            page=request_data.page,
            size=request_data.size,
            db=db,
        )

        cases = [
            TerroristsDataCase(
                id=case.id,
                fio=case.fio,
                birth_place=case.birth_place,
                birth_date=case.birth_date,
            )
            for case in results
        ]
        return cases

    except HTTPException as e:
        logger.warning(f"HTTPException: {e.detail}, статус: {e.status_code}")
        raise e
    except MissingTokenError:
        logger.error("Неавторизованный пользователь")
        raise HTTPException(status_code=401, detail="Неавторизованный пользователь")
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")
