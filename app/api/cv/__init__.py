from fastapi import APIRouter
from .handler import cv_handler

cv_router = APIRouter()

cv_router.add_api_route(
    "/", cv_handler.test, methods=["GET"], summary="Test methods", tags=["test"]
)

cv_router.add_api_route(
    "/", cv_handler.create_cv, methods=["POST"], summary="Create cv", tags=["Create cv"]
)
