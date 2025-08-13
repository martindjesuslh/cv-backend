from fastapi import FastAPI

# from app.api.cv.routes import
#from app.core.config.settings import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title="Cv Backend",
        version="0.1",
        description="Create dynamics Cv"
    )

    

    return app

app = create_app()

    


