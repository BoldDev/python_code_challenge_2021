import uuid
from typing import TYPE_CHECKING, Optional, Union

from pydantic import BaseModel, Extra
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.schemas.base import Base

if TYPE_CHECKING:
    from app.schemas.episode import EpisodeDb


class CommentBase(BaseModel):
    text: str
    episode_id: uuid.UUID

    class Config:
        orm_mode = True


class CommentRead(CommentBase):
    id: uuid.UUID


class CommentCreate(CommentBase, extra=Extra.forbid):
    ...


class CommentUpdate(BaseModel):
    text: Optional[str]


class CommentDb(Base):
    __tablename__ = "comment"

    text: Mapped[str] = mapped_column(nullable=True)

    episode_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("episode.id"),
        default=None,
        nullable=True,
    )

    episode: Mapped["EpisodeDb"] = relationship(
        back_populates="comments",
    )


class CommentsCacheKey(BaseModel):
    method: str
    episode_id: Union[uuid.UUID, None]


class CommentCacheKey(BaseModel):
    method: str
    comment_id: uuid.UUID
