import logging
import uuid
from logging import Logger
from typing import Optional

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.crud.crud_base import CRUDBase
from app.schemas.comment import CommentCreate, CommentDb, CommentUpdate

logger: Logger = logging.getLogger(__name__)


class CRUDComment(
    CRUDBase[
        CommentDb,
        CommentCreate,
        CommentUpdate,
    ]
):
    async def get_multi_by_episode_id(
        self,
        db: AsyncSession,
        episode_id: Optional[uuid.UUID] = None,
        skip: int = 0,
        limit: Optional[int] = None,
    ) -> list[CommentDb]:
        stmt: Select = select(CommentDb)

        if episode_id:
            stmt = stmt.where(CommentDb.episode_id == episode_id)
        result = await db.execute(stmt)
        entries = result.scalars().all()
        return entries


crud_comment = CRUDComment(CommentDb)
