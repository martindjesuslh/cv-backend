from fastapi import APIRouter
from app.api.cv import cv_router

main_router = APIRouter(prefix="/api")


def register_router(router: APIRouter, prefix: str = "", tags: list[str] = None):
    main_router.include_router(router, prefix=prefix, tags=tags or [])


register_router(cv_router, prefix="/cv", tags=["CV"])
