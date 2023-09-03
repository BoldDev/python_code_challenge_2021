from typing import Optional

from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.schemas.http_errors import (
    HTTP400BadRequestResponse,
    HTTP404NotFoundResponse,
)


class HTTP400BadRequestException(Exception):
    def __init__(
        self,
        response: Optional[
            HTTP400BadRequestResponse
        ] = HTTP400BadRequestResponse(),
    ):
        self.response = response


class HTTP404NotFoundException(Exception):
    def __init__(
        self,
        response: Optional[HTTP404NotFoundResponse] = HTTP404NotFoundResponse(),
    ):
        self.response = response


async def http_400_bad_request_exception_handler(
    request: Request, exc: HTTP400BadRequestException
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=exc.response.content.dict(),
        headers=exc.response.headers,
    )


async def http_404_notfound_exception_handler(
    request: Request, exc: HTTP404NotFoundException
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=exc.response.content.dict(),
        headers=exc.response.headers,
    )
