from fastapi import APIRouter

from endpoints.auth import router as auth_router
from endpoints.messages import router as messages_router
from endpoints.users import router as users_router

frontend_api_router = APIRouter()
frontend_api_router.include_router(messages_router, prefix="/messages")
frontend_api_router.include_router(auth_router, prefix="/tokens")
frontend_api_router.include_router(users_router, prefix="/users")
