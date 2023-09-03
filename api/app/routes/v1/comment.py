import logging
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, status

from app.core.config import get_settings
from app.deps.episode import get_episode_service
from app.schemas.comment import CommentCreate, CommentRead, CommentUpdate
from app.schemas.episode import EpisodeRead
from app.schemas.http_errors import (
    HTTP400BadRequestContent,
    HTTP404NotFoundContent,
)
from app.services.episode import EpisodeService

comment_router = APIRouter()
settings = get_settings()
logger = logging.getLogger(__name__)


@comment_router.get(
    "",
    response_model=list[CommentRead],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": HTTP404NotFoundContent,
            "description": "Resource not found",
        },
    },
)
async def list_comments(
    *,
    episode_svc: EpisodeService = Depends(get_episode_service),
    episode_id: Optional[uuid.UUID] = None,
) -> list[EpisodeRead]:
    """List episodes."""
    comments = await episode_svc.list_comments(
        episode_id=episode_id,
    )
    return comments


@comment_router.post("", response_model=CommentRead)
async def create_comment(
    *,
    episode_svc: EpisodeService = Depends(get_episode_service),
    comment: CommentCreate,
) -> CommentRead:
    """Create new comment."""

    comment_read: CommentRead = await episode_svc.create_comment(
        comment=comment,
    )

    return comment_read


@comment_router.get(
    "/{comment_id}",
    response_model=CommentRead,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": HTTP404NotFoundContent,
            "description": "Resource not found",
        },
    },
)
async def retrieve_comment(
    *,
    episode_svc: EpisodeService = Depends(get_episode_service),
    comment_id: uuid.UUID,
) -> CommentRead:
    """
    Get a specific comment by id.
    """

    comment = await episode_svc.get_comment_by_id(comment_id=comment_id)
    return comment


@comment_router.put(
    "/{comment_id}",
    response_model=CommentRead,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": HTTP404NotFoundContent,
            "description": "Resource not found",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": HTTP400BadRequestContent,
            "description": "Bad request",
        },
    },
)
async def update_comment(
    comment_id: uuid.UUID,
    comment: CommentUpdate,
    episode_svc: EpisodeService = Depends(get_episode_service),
) -> CommentRead:
    """
    Update comment.
    """

    comment_read = await episode_svc.update_comment(
        comment_id=comment_id,
        comment=comment,
    )

    return comment_read


@comment_router.delete(
    "/{comment_id}",
    response_model=None,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": HTTP404NotFoundContent,
            "description": "Resource not found",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": HTTP400BadRequestContent,
            "description": "Bad request",
        },
    },
)
async def delete_comment(
    comment_id: uuid.UUID,
    episode_svc: EpisodeService = Depends(get_episode_service),
):
    """
    Delete comment.
    """

    await episode_svc.delete_comment(
        comment_id=comment_id,
    )
