from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import MissingTokenError
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
from loguru import logger


router = APIRouter(prefix="/pledgess", tags=["Irbis/Залоги"])


@router.post("/data", response_model=Optional[List[PledgessGeneralCase]])
async def get_query_data(
    request_data: PledgessDataRequest = Body(...),
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Получает данные о залогах по выполненному запросу."""
    try:
        logger.info(
            f"Запрос court_general_data для query_id: {request_data.query_id}, "
            f"page: {request_data.page}, size: {request_data.size}, "
        )

        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())
        logger.debug(f"Аутентифицированный пользователь: {user_id}")

        irbis_person = await IrbisPersonDAO.get_irbis_person(user_id, request_data.query_id, db)
        if not irbis_person:
            logger.warning(f"Запрос не найден для пользователя {user_id}, query_id: {request_data.query_id}")
            raise HTTPException(status_code=404, detail="Запрос не найден или недоступен")

        logger.debug(f"Найден irbis_person: {irbis_person.id}")

        results = await PledgessDAO.get_paginated_data(
            irbis_person_id=irbis_person.id,
            page=request_data.page,
            size=request_data.size,
            db=db,
        )
        cases = [
            PledgessGeneralCase(
                case_id=case.id,
                pledge_type=case.pledge_type,
                reg_date=case.reg_date,
                pledgers=[
                    PledgessGeneralPledgees(
                        name=party.name,
                    )
                    for party in case.parties if party.type == 'pledgers'
                ],
                pledgees=[
                    PledgessGeneralPledgees(
                        name=party.name,
                    )
                    for party in case.parties if party.type == 'pledgees'
                ],
                pledges=[
                    PledgessGeneralPledges(
                        pledge_type=pledge.pledge_type,
                        pledge_num=pledge.pledge_num,
                    )
                    for pledge in case.pledges
                ]
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


@router.get("/case_full/{case_id}", response_model=PledgessCaseFull)
async def get_full_case_info(
    case_id: int,
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Получает полную информацию о судебном деле по ID дела."""
    try:
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

        case_full = PledgessCaseFull(
            case_id=case.id,
            reg_date=case.reg_date,
            pledge_reestr_number=case.pledge_reestr_number,
            pledge_type=case.pledge_type,

            pledgers=[
                PledgePartiesSchema(
                    name=party.name,
                    birth_date=party.birth_date,
                    inn=party.inn,
                    ogrn=party.ogrn,
                )
                for party in case.parties if party.type == 'pledgers'
            ],
            pledgees=[
                PledgePartiesSchema(
                    name=party.name,
                    type=party.type,
                    inn=party.inn,
                    ogrn=party.ogrn,
                )
                for party in case.parties if party.type == 'pledgees'
            ],
            pledges=[
                PledgeObjectSchema(
                    id=pledge.id,
                    pledge_num_name=pledge.pledge_num_name,
                    pledge_num=pledge.pledge_num,
                    pledge_type=pledge.pledge_type
                )
                for pledge in case.pledges
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
