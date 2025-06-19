import json
import redis
import asyncio
from typing import Dict, List

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