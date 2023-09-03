import logging
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, status

from app.core.config import get_settings
from app.deps.episode import get_episode_service
from app.enums.episode import SeasonNo
from app.schemas.episode import EpisodeRead
from app.schemas.http_errors import HTTP404NotFoundContent
from app.services.episode import EpisodeService

episode_router = APIRouter()
settings = get_settings()
logger = logging.getLogger(__name__)


@episode_router.get(
    "",
    response_model=list[EpisodeRead],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": HTTP404NotFoundContent,
            "description": "Resource not found",
        },
    },
)
async def list_episodes(
    *,
    episode_svc: EpisodeService = Depends(get_episode_service),
    season: Optional[SeasonNo] = None,
    awesome: Optional[bool] = False,
) -> list[EpisodeRead]:
    """List episodes."""
    episodes = await episode_svc.list_episodes(
        season=season,
        awesome=awesome,
    )
    return episodes


@episode_router.get(
    "/{episode_id}",
    response_model=EpisodeRead,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": HTTP404NotFoundContent,
            "description": "Resource not found",
        },
    },
)
async def retrieve_episode(
    *,
    episode_svc: EpisodeService = Depends(get_episode_service),
    episode_id: uuid.UUID,
) -> EpisodeRead:
    """
    Get a specific episode by id.
    """

    # episode = await episode_svc.get_episode_by_imdb_id(imdb_id=episode_id)
    episode = await episode_svc.get_episode_by_id(episode_id=episode_id)
    return episode
