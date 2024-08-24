from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from endpoints import frontend_api_router
from shared.config import settings

origins = ["*"]


def get_app() -> FastAPI:
    app = FastAPI()
    app.title = 'TechStorm'
    app.version = '1.0.0'
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins if settings.is_prod else ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(frontend_api_router, prefix='/api/v1')

    return app
