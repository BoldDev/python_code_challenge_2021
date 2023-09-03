import uuid
from typing import TYPE_CHECKING, Optional, Union

from pydantic import BaseModel, Extra, validator
from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.schemas.base import Base

if TYPE_CHECKING:
    from app.schemas.comment import CommentDb


class EpisodeBase(BaseModel):
    title: str
    season_no: str
    episode_no: str
    rating: float
    imdb_id: str

    @validator("rating", pre=True, always=True)
    def handle_not_applicable(cls, value):
        try:
            value = float(value)
        except ValueError:
            value = -1

        return value

    class Config:
        orm_mode = True


class EpisodeRead(EpisodeBase):
    id: uuid.UUID


class EpisodeCreate(EpisodeBase, extra=Extra.forbid):
    ...


class EpisodeUpdate(BaseModel):
    title: Optional[str]
    season_no: Optional[str]
    episode_no: Optional[str]
    rating: Optional[float]
    imdb_id: Optional[str]


class EpisodeDb(Base):
    __tablename__ = "episode"

    title: Mapped[str] = mapped_column(nullable=True)
    season_no: Mapped[str] = mapped_column(nullable=True)
    episode_no: Mapped[str] = mapped_column(nullable=True)
    rating: Mapped[float] = mapped_column(Numeric(), nullable=True)
    imdb_id: Mapped[str] = mapped_column(nullable=True)

    comments: Mapped[list["CommentDb"]] = relationship(
        back_populates="episode",
    )


class EpisodesCacheKey(BaseModel):
    method: str
    season: Union[str, None]
    awesome: bool


class EpisodeCacheKey(BaseModel):
    method: str
    episode_id: uuid.UUID
