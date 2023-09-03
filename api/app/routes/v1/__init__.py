from fastapi import APIRouter

from .comment import comment_router
from .episode import episode_router

router_v1 = APIRouter()

router_v1.include_router(episode_router, prefix="/episodes", tags=["episodes"])
router_v1.include_router(comment_router, prefix="/comments", tags=["comments"])
