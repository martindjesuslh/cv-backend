from fastapi import APIRouter
from .handlers import test

cv_router = APIRouter()

cv_router.add_api_route(
    "/", test, methods=["GET"], summary="Create cv", tags=["Create cv"]
)
