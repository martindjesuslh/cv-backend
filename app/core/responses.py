from typing import Any, Optional, Dict
from fastapi.responses import JSONResponse
from fastapi import status
from app.schemas.responses import SuccessHttpResponse, ErrorHttpResponse

MESSAGES = {
    "SUCCESS": "Operation completed successfully",
    "CREATED": "Resource created successfully",
    "UPDATED": "Resource updated successfully",
    "DELETED": "Resource deleted successfully",
    "NOT_FOUND": "Resource not found",
    "BAD_REQUEST": "Invalid request data",
    "UNAUTHORIZED": "Authentication required",
    "FORBIDDEN": "Access denied",
    "INTERNAL_ERROR": "Internal server error",
}


class ApiResponse:
    @staticmethod
    def success(
        data: Any = None,
        message: str = None,
        status_code: int = 200,
        meta: Optional[Dict[str, Any]] = None,
    ) -> JSONResponse:
        return JSONResponse(
            content={
                "success": True,
                "message": message or MESSAGES["SUCCESS"],
                "data": data,
                "meta": meta,
            },
            status_code=status_code,
        )

    @staticmethod
    def error(
        message: str = None,
        status_code: int = 500,
        error_code: Optional[str] = None,
        details: Any = None,
    ) -> JSONResponse:
        """Error response"""
        return JSONResponse(
            {
                "success": False,
                "message": message or MESSAGES["INTERNAL_ERROR"],
                "error_code": error_code,
                "details": details,
                "status_code": status_code,
            },
            status_code=status_code,
        )


# helpers
def ok(data: Any = None, message: str = None, meta: Optional[Dict[str, Any]] = None):
    return ApiResponse.success(
        data=data, message=message, status_code=status.HTTP_200_OK, meta=meta
    )


def not_found(message: str = None):
    return ApiResponse.error(
        message=message or MESSAGES["NOT_FOUND"],
        status_code=404,
        error_code="NOT_FOUND",
    )


def bad_request(message: str = None, details: Any = None):
    return ApiResponse.error(
        message=message or MESSAGES["BAD_REQUEST"],
        error_code="BAD REQUEST",
        status_code=400,
        details=details,
    )
