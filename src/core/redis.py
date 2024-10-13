import json
from typing import Optional, Union, List
from fastapi.encoders import jsonable_encoder

import redis.asyncio as redis
from redis.asyncio.client import Redis

from .config import config


async def get_redis() -> Redis:
    return redis.from_url(config.REDIS_URL, encoding="utf-8", decode_responses=True)

async def set_redis_value(redis_instance: Redis, key: str, data: Union[dict, List[dict]], ttl: int):
    await redis_instance.set(key, json.dumps(data), ex=ttl)

async def get_redis_value(redis_instance: Redis, key: str) -> Optional[dict]:
    data = await redis_instance.get(key)
    if data:
        return json.loads(data)
    return None

async def delete_redis_value(redis_instance: Redis, key: str) -> None:
    await redis_instance.delete(key)