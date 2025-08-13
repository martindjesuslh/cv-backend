from typing import Any, Optional, Dict, TypeVar, Generic
from pydantic import BaseModel

T = TypeVar("T")


class BaseHttpResponse(BaseModel):
    success: bool
    status_code: int


class SuccessHttpResponse(BaseHttpResponse, Generic[T]):
    data: Optional[T] = None
    message: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None


class ErrorHttpResponse(BaseHttpResponse):
    error: str
    error_code: Optional[str] = None
    details: Optional[Any] = None
