from fastapi import APIRouter
from app.routers.users import router as users_router
from app.routers.health import router as health_router

api_router = APIRouter(prefix="/api")

api_router.include_router(users_router, tags=["users"])
api_router.include_router(health_router, tags=["system"])
