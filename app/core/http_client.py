import httpx
from typing import Any, Optional, Dict, TypeVar, Type, Union
from pydantic import BaseModel
from app.core.schemas.responses import SuccessHttpResponse, ErrorHttpResponse
from app.core.config.settings import settings

T = TypeVar("T", bound=BaseModel)


class _ApiClient:
    """Client for making requests to external APIs with consistent error handling."""

    def __init__(self, base_url: str = None, timeout: int = None):
        self.base_url = (base_url or settings.API_BASE_URL).rstrip("/")
        self.timeout = timeout or settings.REQUEST_TIMEOUT
        self.client = httpx.AsyncClient(timeout=timeout)

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        response_model: Type[T],
        data: Optional[BaseModel] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> Union[SuccessHttpResponse[T], ErrorHttpResponse]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        request_timeout = timeout or self.timeout

        try:
            json_data = data.model_dump() if data else None

            response = await getattr(self.client, method.lower())(
                url,
                json=json_data,
                params=params,
                headers=headers,
                timeout=request_timeout,
            )
            return await self.__handle_response(response, response_model)

        except httpx.TimeoutException:
            return ErrorHttpResponse(
                success=False,
                status_code=408,
                error="Request timeout",
                error_code="TIMEOUT_ERROR",
                details=f"{method.upper()} request to {endpoint} timed out after {request_timeout} seconds",
            )
        except httpx.RequestError as e:
            return ErrorHttpResponse(
                success=False,
                status_code=500,
                error="Request error",
                error_code="REQUEST_ERROR",
                details=str(e),
            )
        except Exception as e:
            return ErrorHttpResponse(
                success=False,
                status_code=500,
                error="Internal error",
                error_code="INTERNAL_ERROR",
                details=str(e),
            )

    async def __handle_response(
        self, response, response_model: Type[T]
    ) -> Union[SuccessHttpResponse[T], ErrorHttpResponse]:
        if 200 <= response.status_code < 300:
            try:
                response_json = response.json() if response.content else {}
                parsed_data = response_model.model_validate(response_json)

                return SuccessHttpResponse(
                    success=True, status_code=response.status_code, data=parsed_data
                )
            except Exception as e:
                return ErrorHttpResponse(
                    success=False,
                    status_code=500,
                    error="Failed to parse response data",
                    error_code="PARSE_ERROR",
                    details=str(e),
                )
        else:
            return ErrorHttpResponse(
                success=False,
                status_code=response.status_code,
                error="Request failed with HTTP error",
                error_code=f"HTTP_{response.status_code}",
                details=response.text,
            )

    def _get_success_message(self, status_code: int) -> str:
        messages = {
            201: settings.MESSAGES_RESPONSE["CREATED"],
            204: settings.MESSAGES_RESPONSE["DELETED"],
        }
        return messages.get(status_code, settings.MESSAGES_RESPONSE["CREATED"])

    async def get(
        self,
        endpoint: str,
        response_model: Type[T],
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> Union[SuccessHttpResponse[T], ErrorHttpResponse]:
        return await self._make_request(
            method="GET",
            endpoint=endpoint,
            response_model=response_model,
            params=params,
            headers=headers,
            timeout=timeout,
        )

    async def post(
        self,
        endpoint: str,
        data: BaseModel,
        response_model: Type[T],
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> Union[SuccessHttpResponse[T], ErrorHttpResponse]:
        return await self._make_request(
            method="POST",
            endpoint=endpoint,
            response_model=response_model,
            data=data,
            headers=headers,
            timeout=timeout,
        )


api_client = _ApiClient(
    base_url=settings.API_BASE_URL, timeout=settings.REQUEST_TIMEOUT
)
