import asyncio
from loguru import logger
from fastapi.responses import StreamingResponse
from fastapi import (
    FastAPI,
    Request,
    Depends,
    HTTPException
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, func

from server.api.routers.auth import router as auth_router
from server.api.routers.users import router as user_router
from server.api.routers.query import router as query_router
from server.api.routers.telegram import router as telegram_router
from server.api.routers.irbis import router as irbis_router
from server.api.routers.admin import router as admin_router, setup_admin
from server.api.scripts.sse_manager import (
    event_generator,
    add_subscriber,
    redis_listener,
)
from server.api.services.file_storage import FileStorageService
from server.api.database.database import get_db
from server.api.models.models import Users
import server.tasks.logger  # noqa: F401


def get_file_storage() -> FileStorageService:
    return FileStorageService()


app = FastAPI()
app.dependency_overrides[FileStorageService] = get_file_storage

setup_admin(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix='/api')
app.include_router(user_router, prefix='/api')
app.include_router(query_router, prefix='/api')
app.include_router(telegram_router, prefix='/api')
app.include_router(admin_router, prefix='/api')
app.include_router(irbis_router, prefix='/api')


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(redis_listener())
    logger.info('Сервер запущен')


@app.get("/api/sse/{channel}")
async def sse_endpoint(
    channel: str,
    request: Request,
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_db)
):
    try:
        Authorize.jwt_required()
        user_id = int(Authorize.get_jwt_subject())
    except Exception:
        raise HTTPException(status_code=401, detail="Not authorized")

    try:
        await db.execute(
            update(Users)
            .where(Users.id == user_id)
            .values(last_visited=func.now())
        )
        await db.commit()
    except Exception as e:
        logger.error(f"Ошибка обновления последнего посещения: {e}")
        await db.rollback()

    queue = asyncio.Queue()
    await add_subscriber(channel, queue)
    return StreamingResponse(
        event_generator(channel, queue, request),
        media_type="text/event-stream",
    )

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_config=None)
