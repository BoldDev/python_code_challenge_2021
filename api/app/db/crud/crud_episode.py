import logging

# import uuid
from logging import Logger
from typing import Optional

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.const import AWESOME_RATING_THRESHOLD
from app.db.crud.crud_base import CRUDBase
from app.enums.episode import SeasonNo
from app.schemas.episode import EpisodeCreate, EpisodeDb, EpisodeUpdate

# from typing import Optional

# from sqlalchemy import Select, Selectable
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select
# from sqlalchemy.sql.expression import func


logger: Logger = logging.getLogger(__name__)


class CRUDEpisode(
    CRUDBase[
        EpisodeDb,
        EpisodeCreate,
        EpisodeUpdate,
    ]
):
    async def get_multi_by_season_by_awesomeness(
        self,
        db: AsyncSession,
        season: Optional[SeasonNo] = None,
        awesome: Optional[bool] = False,
        skip: int = 0,
        limit: Optional[int] = None,
    ) -> list[EpisodeDb]:
        stmt: Select = select(EpisodeDb)

        if season:
            stmt = stmt.where(EpisodeDb.season_no == season.value)

        if awesome:
            stmt = stmt.where(EpisodeDb.rating > AWESOME_RATING_THRESHOLD)

        result = await db.execute(stmt)
        entries = result.scalars().all()
        return entries

    async def get_by_imdb_id(
        self,
        db: AsyncSession,
        imdb_id: str,
    ) -> EpisodeDb:
        stmt: Select = select(EpisodeDb).where(EpisodeDb.imdb_id == imdb_id)
        result = await db.execute(stmt)
        entry = result.scalar_one_or_none()
        return entry

    #     stmt_count = (
    #         select(func.count())
    #         .select_from(UrlDb)
    #         .join(UrlDb.users)
    #         .where(
    #             UserDb.id == user_id,
    #         )
    #     )

    #     # stmt_count = (
    #     #     select(func.count())
    #     #     .select_from(self.model)
    #     #     .where(
    #     #         user_id
    #     #         # user_id in UrlDb.users
    #     #         # UrlDb.user_id == user_id,
    #     #     )
    #     # )
    #     count_result = await db.execute(stmt_count)
    #     count = count_result.scalar_one()

    #     # stmt = select(self.model).where(UrlDb.user_id == user_id).offset(skip)

    #     if limit:
    #         stmt = stmt.limit(limit)
    #     result = await db.execute(stmt)
    #     entries = result.scalars().unique().all()
    #     return self.list_model(data=entries, count=count)

    # async def create_with_users(
    #     self,
    #     db: AsyncSession,
    #     obj_in: UrlDbCreate,
    #     users: list[UserDb],
    #     flush: bool = True,
    #     commit: bool = False,
    #     refresh: bool = False,
    # ) -> UrlDb:
    #     url: UrlDb = await self.create(
    #         db=db,
    #         obj_in=obj_in,
    #         flush=False,
    #     )
    #     url.users = users

    #     if flush:
    #         await db.flush()

    #     if commit:
    #         await db.commit()

    #     if refresh and (flush or commit):
    #         await db.refresh(users)

    #     return url


crud_episode = CRUDEpisode(EpisodeDb)
