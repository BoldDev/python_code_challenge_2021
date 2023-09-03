import asyncio
import itertools as it
import uuid
from typing import Optional

from aioredis import Redis
from pydantic import parse_obj_as, parse_raw_as
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    HTTP400BadRequestException,
    HTTP404NotFoundException,
)
from app.db.crud.crud_comment import crud_comment
from app.db.crud.crud_episode import crud_episode
from app.enums.episode import SeasonNo
from app.schemas.comment import (
    CommentCacheKey,
    CommentCreate,
    CommentDb,
    CommentRead,
    CommentsCacheKey,
    CommentUpdate,
)
from app.schemas.episode import (
    EpisodeCacheKey,
    EpisodeCreate,
    EpisodeDb,
    EpisodeRead,
    EpisodesCacheKey,
)
from app.schemas.http_errors import (
    HTTP400BadRequestResponse,
    HTTP404NotFoundContent,
)
from app.services.base import BaseService


class EpisodeService(BaseService):
    def __init__(
        self,
        db: AsyncSession,
        redis: Redis,
    ) -> None:
        super().__init__(db=db)
        self.redis = redis

    async def create_episode(
        self,
        episode: EpisodeCreate,
    ) -> EpisodeRead:
        episode_db: EpisodeDb = await crud_episode.create(
            db=self.db,
            obj_in=episode,
            commit=True,
        )

        return episode_db

    async def create_all_episodes(
        self,
        episodes: list[EpisodeCreate],
    ) -> list[EpisodeRead]:
        await crud_episode.delete_all(db=self.db)
        await self.redis.flushdb()
        episodes_db = await crud_episode.create_multi(
            db=self.db,
            objs_in=episodes,
            commit=True,
        )

        seasons = [i for i in SeasonNo] + [None]
        awesomes = [True, False]
        list_episodes_args = it.product(seasons, awesomes)

        list_episodes_futs = [
            self.list_episodes(season, awesome)
            for season, awesome in list_episodes_args
        ]

        retrieve_episode_futs = [
            self.get_episode_by_id(episode_id=episode.id) for episode in episodes_db
        ]

        await asyncio.gather(
            *(list_episodes_futs + retrieve_episode_futs),
        )

        return episodes

    async def list_episodes(
        self,
        season: Optional[SeasonNo] = None,
        awesome: Optional[bool] = False,
    ) -> list[EpisodeRead]:
        episodes_cache_key = EpisodesCacheKey(
            method="list", season=season, awesome=awesome
        ).json()
        episodes_cached = await self.redis.lrange(episodes_cache_key, 0, -1)
        if episodes_cached:
            episodes = [
                parse_raw_as(EpisodeRead, episode_cached)
                for episode_cached in episodes_cached
            ]

        else:
            episodes_db = await crud_episode.get_multi_by_season_by_awesomeness(
                db=self.db,
                season=season,
                awesome=awesome,
            )
            episodes = parse_obj_as(list[EpisodeRead], episodes_db)

            for episode in episodes:
                episode_json = episode.json()
                await self.redis.rpush(episodes_cache_key, episode_json)
        return episodes

    async def get_episode_by_id(
        self,
        episode_id: str,
    ) -> EpisodeRead:
        episode_cache_key = EpisodeCacheKey(
            method="retrieve", episode_id=episode_id
        ).json()
        episode_cached = await self.redis.get(episode_cache_key)
        if episode_cached:
            episode = parse_raw_as(EpisodeRead, episode_cached)
        else:
            episode_db = await crud_episode.get(
                db=self.db,
                id=episode_id,
            )
            if not episode_db:
                raise HTTP404NotFoundException()
                # raise HTTPException(status_code=404, detail="Not found")
            episode = parse_obj_as(EpisodeRead, episode_db)
            episode_json = episode.json()
            await self.redis.set(episode_cache_key, episode_json)
        return episode

    async def list_comments(
        self,
        episode_id: Optional[uuid.UUID] = None,
    ) -> list[CommentRead]:
        comments_cache_key = CommentsCacheKey(
            method="list",
            episode_id=episode_id,
        ).json()
        comments_cached = await self.redis.lrange(comments_cache_key, 0, -1)
        if comments_cached:
            comments = [
                parse_raw_as(CommentRead, comment_cached)
                for comment_cached in comments_cached
            ]

        else:
            comments_db = await crud_comment.get_multi_by_episode_id(
                db=self.db,
                episode_id=episode_id,
            )
            comments = parse_obj_as(list[CommentRead], comments_db)

        return comments

    async def create_comment(
        self,
        comment: CommentCreate,
    ) -> CommentRead:
        episode_db: EpisodeDb = await crud_episode.get(
            db=self.db,
            id=comment.episode_id,
        )
        if not episode_db:
            raise HTTP400BadRequestException(
                response=HTTP400BadRequestResponse(
                    content=HTTP404NotFoundContent(
                        msg=f"Bad episode [{comment.episode_id=}]"
                    )
                )
            )

        comment_db: CommentDb = await crud_comment.create(
            db=self.db,
            obj_in=comment,
            # episode=episode_db,
            commit=True,
        )

        comment_read = parse_obj_as(CommentRead, comment_db)

        comment_cache_key = CommentCacheKey(
            method="retrieve", comment_id=comment_read.id
        ).json()
        comment_json = comment_read.json()
        await self.redis.set(comment_cache_key, comment_json)

        comments_cache_key = CommentsCacheKey(
            method="list",
            episode_id=comment_read.episode_id,
        ).json()
        await self.redis.rpush(comments_cache_key, comment_json)

        return comment_read

    async def get_comment_by_id(
        self,
        comment_id: uuid.UUID,
    ) -> CommentRead:
        comment_cache_key = CommentCacheKey(
            method="retrieve", comment_id=comment_id
        ).json()
        comment_cached = await self.redis.get(comment_cache_key)

        if comment_cached:
            comment = parse_raw_as(CommentRead, comment_cached)
        else:
            comment_db = await crud_comment.get(
                db=self.db,
                id=comment_id,
            )
            if not comment_db:
                raise HTTP404NotFoundException()
            comment = parse_obj_as(CommentRead, comment_db)
        return comment

    async def update_comment(
        self,
        comment_id: uuid.UUID,
        comment: CommentUpdate,
    ) -> CommentRead:
        # await crud_comment.get()

        comment_db = await crud_comment.get(
            db=self.db,
            id=comment_id,
        )

        comment_updated_db = await crud_comment.update(
            db=self.db,
            db_obj=comment_db,
            obj_in=comment,
            commit=True,
        )

        comment_read = parse_obj_as(CommentRead, comment_updated_db)
        comment_json = comment_read.json()

        comment_cache_key = CommentCacheKey(
            method="retrieve",
            comment_id=comment_read.id,
        ).json()
        await self.redis.set(comment_cache_key, comment_json)

        # TODO: implement update cache (method="list")

        return comment_read

    async def delete_comment(
        self,
        comment_id: uuid.UUID,
    ):
        await crud_comment.delete(
            db=self.db,
            id=comment_id,
        )
        await self.db.commit()

        comment_cache_key = CommentCacheKey(
            method="retrieve",
            comment_id=comment_id,
        ).json()
        await self.redis.delete(comment_cache_key)

        # TODO: implement cache update (method="list")


# Facade #############################


async def create_episode_service(
    db: AsyncSession,
    redis: Redis,
) -> EpisodeService:
    episode_svc: EpisodeService = EpisodeService(
        db=db,
        redis=redis,
    )
    return episode_svc
