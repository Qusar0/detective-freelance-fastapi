from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from server.api.handlers.auth import router as auth_router
from server.api.handlers.users import router as user_router
from server.api.handlers.query import router as query_router
from server.api.handlers.telegram import router as telegram_router
from fastapi.responses import StreamingResponse
import asyncio
from typing import Dict, List
import json
import redis

app = FastAPI()

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


subscribers: Dict[str, List[asyncio.Queue]] = {}

r = redis.StrictRedis(host='localhost', port=6379, db=0, password="1")


async def event_generator(channel: str, queue: asyncio.Queue, request: Request):
    try:
        while True:
            if await request.is_disconnected():
                break
            try:
                # Wait for data to be sent to the queue (i.e., new SSE message)
                data = await asyncio.wait_for(queue.get(), timeout=5.0)
                yield f"data: {data}\n\n"
            except asyncio.TimeoutError:
                yield ": ping\n\n"
    finally:
        # Remove queue from subscribers when disconnected
        subscribers[channel].remove(queue)


@app.get("/sse/{channel}")
async def sse_endpoint(channel: str, request: Request):
    queue = asyncio.Queue()
    subscribers.setdefault(channel, []).append(queue)
    return StreamingResponse(
        event_generator(channel, queue, request),
        media_type="text/event-stream",
    )


async def publish_event(channel: str, data: dict):
    message = json.dumps(data)
    if channel in subscribers:
        for queue in subscribers[channel]:
            await queue.put(message)

    r.publish(channel, message)


async def redis_listener():
    pubsub = r.pubsub()
    pubsub.subscribe(*subscribers.keys())
    while True:
        message = pubsub.get_message()
        if message:
            if message['type'] == 'message':
                channel = message['channel']
                data = json.loads(message['data'])
                print(channel)
                print(data)
                print(subscribers)
                if channel in subscribers:
                    for queue in subscribers[channel]:
                        await queue.put(data)
        await asyncio.sleep(0.1)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(redis_listener())


@app.post("/publish/{channel}")
async def publish(channel: str, data: dict):
    await publish_event(channel, data)
    return {"message": "Event published", "channel": channel, "data": data}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
