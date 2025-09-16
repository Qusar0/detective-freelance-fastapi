from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import MissingTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from server.api.database.database import get_db
from server.api.schemas.irbis.irbis_general import (
    RegionInfo,
    IrbisPersonInfo,
)
from typing import List
from server.api.dao.irbis.irbis_person import IrbisPersonDAO
from server.api.dao.irbis.region_subjects import RegionSubjectDAO
from server.api.routers.irbis.court_general import router as court_general_router
from server.api.routers.irbis.arbitration_court import router as arbitration_court_router
from server.api.routers.irbis.bankruptcy import router as bankruptcy_router
from server.api.routers.irbis.disqualified_person import router as disqualified_person_router
from server.api.routers.irbis.pledgess import router as pledgess_router
from server.api.routers.irbis.corruption import router as corruption_router
from server.api.routers.irbis.fssp import router as fssp_router
from loguru import logger


router = APIRouter(
    prefix="/irbis",
    tags=["Irbis"]
)

router.include_router(court_general_router)
router.include_router(arbitration_court_router)
router.include_router(bankruptcy_router)
router.include_router(disqualified_person_router)
router.include_router(pledgess_router)
router.include_router(corruption_router)
router.include_router(fssp_router)


@router.get("/regions", response_model=List[RegionInfo], tags=['Irbis/Общее'])
async def get_regions(db: AsyncSession = Depends(get_db)):
    """Получает информацию о всех регионах РФ."""
    try:
        regions = await RegionSubjectDAO.find_all(db)
        return [
            RegionInfo(
                id=region.subject_number,
                name=region.name,
            )
            for region in regions
        ]
    except HTTPException as e:
        logger.warning(f"HTTPException: {e.detail}, статус: {e.status_code}")
        raise e
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.get("/person_info/{query_id}", response_model=IrbisPersonInfo, tags=['Irbis/Общее'])
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
                    id=region.id,
                    name=region.name,
                )
                for region in regions
            ]
        )

        logger.success(f"Успешно возвращена информация о человеке: {irbis_person.fullname}")
        return person_info

    except HTTPException as e:
        logger.warning(f"HTTPException: {e.detail}, статус: {e.status_code}")
        raise e
    except MissingTokenError:
        logger.error('Неавторизованный пользователь')
        raise HTTPException(status_code=401, detail="Неавторизованный пользователь")
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")
