from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from server.api.database.database import get_db
from server.api.schemas.irbis import (
    CourtGeneralCase,
    IrbisDataRequest,
    CourtGeneralFace,
    CourtGeneralProgress,
)

from server.api.dao.irbis.person_uuid import IrbisPersonDAO
from server.api.dao.irbis.court_general_jur import CourtGeneralJurDAO


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
        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())

        irbis_person = await IrbisPersonDAO.get_irbis_person(user_id, request_data.query_id, db)
        if not irbis_person:
            raise HTTPException(status_code=404, detail="Запрос не найден или недоступен")

        results = await CourtGeneralJurDAO.get_paginated_query_data(
            irbis_person_id=irbis_person.id,
            page=request_data.page,
            size=request_data.size,
            db=db,
        )

        cases = []
        for case in results:
            faces = []
            progresses = []
            for face in case.faces:
                faces.append(
                    CourtGeneralFace(
                        role=face.role,
                        face=face.face,
                        role_name=face.role_name,
                    )
                )
            for progress in case.progress:
                progresses.append(
                    CourtGeneralProgress(
                        name=progress.name,
                        progress_data=progress.progress_date,
                        resolution=progress.resolution,
                    )
                )
            cases.append(
                CourtGeneralCase(
                    case_number=case.case_number,
                    court_name=case.court_name,
                    start_date=case.start_date,
                    end_date=case.end_date,
                    review=case.review,
                    region=case.region,
                    process_type=case.process_type,
                    judge=case.judge,
                    papers=case.papers,
                    papers_pretty=case.papers_pretty,
                    links=case.links,
                    progress=progresses,
                    faces=faces,
                )
            )
        return cases
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e
