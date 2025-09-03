import asyncio
from loguru import logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.api.routers.auth import router as auth_router
from server.api.routers.users import router as user_router
from server.api.routers.query import router as query_router
from server.api.routers.telegram import router as telegram_router
from server.api.routers.irbis.irbis_general import router as irbis_router
from server.api.routers.sse import router as sse_router
from server.api.routers.admin import router as admin_router, setup_admin
from server.api.scripts.sse_manager import redis_listener
from server.api.services.file_storage import FileStorageService, get_file_storage


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
app.include_router(sse_router, prefix='/api')


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(redis_listener())
    logger.info('Сервер запущен')


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_config=None)
