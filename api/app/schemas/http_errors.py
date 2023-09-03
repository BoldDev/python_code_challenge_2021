from typing import Dict, Optional, Union

from pydantic import BaseModel


class HTTP400BadRequestContent(BaseModel):
    code: str = "HTTP_400"
    msg: str = "Bad request"


class HTTP404NotFoundContent(BaseModel):
    code: str = "HTTP_404"
    msg: str = "Resource not found"


# HTTP Errors Response Schemas
# ############################
class HTTP400BadRequestResponse(BaseModel):
    content: Optional[HTTP400BadRequestContent] = HTTP400BadRequestContent()
    headers: Optional[Union[Dict[str, str], None]] = None


class HTTP404NotFoundResponse(BaseModel):
    content: Optional[HTTP404NotFoundContent] = HTTP404NotFoundContent()
    headers: Optional[Union[Dict[str, str], None]] = None
