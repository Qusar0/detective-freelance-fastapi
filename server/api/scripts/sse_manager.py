import json
import redis
import asyncio
import base64
from typing import Dict, List
from sqlalchemy import select

from server.api.models.models import Users
from server.api.database.database import get_db
from server.api.dao.events import EventsDAO
from server.api.conf.config import settings


r = redis.StrictRedis.from_url(settings.redis_url)

subscribers: Dict[str, List[asyncio.Queue]] = {}

async def publish_event(channel: str, data: dict):
    message = json.dumps(data)
    
    if channel in subscribers:
        for queue in subscribers[channel]:
            await queue.put(data)
    
    r.publish(channel, message)


async def event_generator(channel: str, queue: asyncio.Queue, request):
    try:
        while True:
            if await request.is_disconnected():
                break
            try:
                data = await asyncio.wait_for(queue.get(), timeout=5.0)
                json_data = json.dumps(data)
                yield f'data: {json_data}\n\n'
            except asyncio.TimeoutError:
                yield ': ping\n\n'
    finally:
        if channel in subscribers:
            subscribers[channel].remove(queue)


async def add_subscriber(channel: str, queue: asyncio.Queue):
    subscribers.setdefault(channel, []).append(queue)


async def redis_listener():
    pubsub = r.pubsub()
    
    while True:
        channels = list(subscribers.keys())
        
        if channels:
            pubsub.subscribe(*channels)
            
            while True:
                message = pubsub.get_message()
                if message and message['type'] == 'message':
                    channel = message['channel'].decode('utf-8')
                    try:
                        data = json.loads(message['data'])
                        if channel in subscribers:
                            for queue in subscribers[channel]:
                                await queue.put(data)
                    except json.JSONDecodeError:
                        print(f'Error decoding JSON from Redis: {message["data"]}')
                await asyncio.sleep(0.1)
        else:
            await asyncio.sleep(1) 


async def send_sse_notification(user_query, channel, db):
    event_data = {
        "message": {
            "status": user_query.query_status,
            "task_id": user_query.query_id,
            "task_category": user_query.query_category,
            "task_title": user_query.query_title,
            "task_created_at": str(user_query.query_created_at)
        }
    }

    event_id, event_type, created_time, event_status = await EventsDAO.save_event(
        event_data,
        user_query.query_id,
        db,
    )

    event_data.update({
        "event_id": event_id,
        "event_type": event_type,
        "created_time": str(created_time),
        "event_status": event_status
    })

    await publish_event(channel, event_data)


async def generate_sse_message_type(user_id: int, db=None) -> str:
    query = select(Users).filter_by(id=user_id)
    if not db:
        async with get_db() as db:
            result = await db.execute(query)
    else:
        result = await db.execute(query)

    user = result.scalar_one_or_none()

    if user is None:
        raise ValueError(f"User with id {user_id} not found")

    email = user.email
    created_time = str(user.created)

    message_type = f"{email}{created_time}"
    base64_string = base64.b64encode(
        message_type.encode("ascii"),
    ).decode("ascii")

    return base64_string