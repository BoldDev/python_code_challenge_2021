import asyncio

import aioredis
import typer

from app.const import SEASONS_TOTAL_NUM
from app.core.config import get_settings
from app.db.crud.crud_comment import crud_comment
from app.db.crud.crud_episode import crud_episode
from app.db.session import async_session_factory
from app.schemas.episode import EpisodeCreate
from app.services.episode import create_episode_service
from app.utils.omdb_client import get_season
from app.utils.omdb_client.schemas import Season

episode = typer.Typer(name="episode", add_completion=False)


@episode.command()
def fetch() -> None:
    asyncio.run(afetch())


@episode.command()
def prune(
    cache: bool = False,
    database: bool = False,
    all: bool = False,
) -> None:
    asyncio.run(aprune(cache, database, all))


async def aprune(cache: bool, database: bool, all: bool):
    settings = get_settings()
    # flush cache db
    if cache or all:
        print("Deleting cache...")
        redis = await aioredis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0",
            decode_responses=True,
        )

        await redis.flushdb()

    if database or all:
        print("Deleting database...")
        async with async_session_factory() as db:
            await crud_comment.delete_all(db=db)
            await crud_episode.delete_all(db=db)
            await db.commit()
    print("DONE")


async def afetch():
    print("Fetching episodes...")
    settings = get_settings()

    redis = await aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0",
        decode_responses=True,
    )

    futs = [
        get_season(
            api_key=settings.OMDB_API_KEY,
            season_no=str(i),
        )
        for i in range(1, SEASONS_TOTAL_NUM + 1)
    ]
    seasons: list[Season] = await asyncio.gather(*futs)
    episodes: list[EpisodeCreate] = [
        EpisodeCreate(
            title=episode.Title,
            episode_no=episode.Episode,
            imdb_id=episode.imdbID,
            rating=episode.imdbRating,
            season_no=season.Season,
        )
        for season in seasons
        for episode in season.Episodes
    ]

    async with async_session_factory() as db:
        episode_svc = await create_episode_service(
            db=db,
            redis=redis,
        )
        await episode_svc.create_all_episodes(
            episodes=episodes,
        )

    print("DONE")
