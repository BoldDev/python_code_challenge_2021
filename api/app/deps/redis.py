import aioredis

from app.core.config import Settings, get_settings

settings: Settings = get_settings()


# async def get_redis():
#     redis = await aioredis.from_url(
#         f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0",
#         decode_responses=True,
#     )
#     return redis


async def get_redis():
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0",
        decode_responses=True,
    )
    async with redis.client() as conn:
        yield conn
