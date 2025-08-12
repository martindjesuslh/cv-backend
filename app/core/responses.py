from typing import Any, Optional, Dict
from fastapi.responses import JSONResponse
from app.schemas.responses import SuccessHttpResponse, ErrorHttpResponse
from app.core.settings import settings


class _ApiResponse:
    @staticmethod
    def _success(
        data: Any = None,
        message: str = None,
        status_code: int = 200,
        meta: Optional[Dict[str, Any]] = None,
    ) -> JSONResponse:
        response = SuccessHttpResponse(
            success=True,
            status_code=status_code,
            data=data,
            message=message or settings.MESSAGES_RESPONSE["SUCCESS"],
            meta=meta,
        )

        return JSONResponse(
            content=response.model_dump(),
            status_code=status_code,
        )

    @staticmethod
    def _error(
        message: str = None,
        status_code: int = 500,
        error_code: Optional[str] = None,
        details: Any = None,
    ) -> JSONResponse:
        """Error response"""
        response = ErrorHttpResponse(
            success=False,
            status_code=status_code,
            error=message or settings.MESSAGES_RESPONSE["INTERNAL_ERROR"],
            error_code=error_code,
            details=details,
        )
        return JSONResponse(
            content=response.model_dump(),
            status_code=status_code,
        )


# helpers
def ok(data: Any = None, message: str = None, meta: Optional[Dict[str, Any]] = None):
    return _ApiResponse._success(data=data, message=message, status_code=200, meta=meta)


def internal_error(message: str = None, details: Any = None):
    return _ApiResponse._error(
        message=message or settings.MESSAGES_RESPONSE["INTERNAL_ERROR"],
        status_code=500,
        details=details,
        error_code="INTERNAL_ERROR",
    )


def not_found(message: str = None):
    return _ApiResponse._error(
        message=message or settings.MESSAGES_RESPONSE["NOT_FOUND"],
        status_code=404,
        error_code="NOT_FOUND",
    )


def bad_request(message: str = None, details: Any = None):
    return _ApiResponse._error(
        message=message or settings.MESSAGES_RESPONSE["BAD_REQUEST"],
        error_code="BAD REQUEST",
        status_code=400,
        details=details,
    )
