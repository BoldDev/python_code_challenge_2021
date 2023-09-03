from aioredis import Redis
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.deps.redis import get_redis
from app.services.episode import create_episode_service


async def get_episode_service(
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    episode_svc = await create_episode_service(
        db=db,
        redis=redis,
    )
    return episode_svc
