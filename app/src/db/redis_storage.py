from typing import Any, Generator

from redis.asyncio import Redis

def get_redis(host: str, port: int, db: int = 1) -> Generator[Any, Any, Redis]:
    redis = Redis(host=host, port=port, db=db, decode_responses=True)
    yield redis
    redis.close()
