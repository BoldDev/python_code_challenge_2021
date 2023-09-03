import logging
from pprint import pformat

import uvicorn
from fastapi import FastAPI, status
from starlette.middleware.cors import CORSMiddleware

from app.core.config import Settings, get_settings
from app.core.exceptions import (
    HTTP400BadRequestException,
    HTTP404NotFoundException,
    http_400_bad_request_exception_handler,
    http_404_notfound_exception_handler,
)
from app.core.logging import setup_logger
from app.db.sanity import check_db_is_ready
from app.db.session import close_engine
from app.routes.v1 import router_v1

logger: logging.Logger = logging.getLogger(__name__)
settings: Settings = get_settings()


app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    # middleware=middleware,
)

if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        # allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
        allow_origins=[
            "*",
            "http://api",
            "http://api:9000",
            "http://localhost",
            "http://localhost:9000",
            "http://localhost:3000",
            "http://web",
            "http://web:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# setup logging
@app.on_event("startup")
async def startup_event() -> None:
    setup_logger()
    root_logger: logging.Logger = logging.getLogger()
    root_logger.debug("======== Logging setup! ========")
    if settings.DEBUG:
        root_logger.info(pformat(settings.dict()))

    await check_db_is_ready()


@app.on_event("shutdown")
async def shutdown_event():
    root_logger = logging.getLogger()
    root_logger.debug("Disposing db engine...")
    await close_engine()
    root_logger.debug("======== Terminated! ========")


app.add_exception_handler(
    HTTP400BadRequestException,
    http_400_bad_request_exception_handler,
)
app.add_exception_handler(
    HTTP404NotFoundException,
    http_404_notfound_exception_handler,
)


@app.get("/", status_code=status.HTTP_200_OK, tags=["health-check"])
async def health_check():
    return ""


app.include_router(router_v1, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    uvicorn.run(
        settings.API_APP,
        host="0.0.0.0",
        reload=True,
        port=settings.PORT,
        # log_config=uvicorn_log_config,
    )
