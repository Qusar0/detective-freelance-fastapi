from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from server.api.handlers.auth import router as auth_router
from server.api.handlers.users import router as user_router
from server.api.handlers.query import router as query_router
from server.api.handlers.telegram import router as telegram_router
from server.api.admin.router import router as admin_router, setup_admin
from fastapi.responses import StreamingResponse
import asyncio
from server.api.scripts.sse_manager import (
    event_generator,
    add_subscriber,
    redis_listener,
)

app = FastAPI()


setup_admin(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(query_router)
app.include_router(telegram_router)
app.include_router(admin_router)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(redis_listener())

@app.get("/sse/{channel}")
async def sse_endpoint(channel: str, request: Request):
    queue = asyncio.Queue()
    await add_subscriber(channel, queue)
    return StreamingResponse(
        event_generator(channel, queue, request),
        media_type="text/event-stream",
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
