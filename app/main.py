from fastapi import FastAPI
from app.api import main_router


def create_app() -> FastAPI:
    app = FastAPI(title="Cv Backend", version="0.1", description="Create dynamics Cv")
    app.include_router(main_router)
    return app


app = create_app()
