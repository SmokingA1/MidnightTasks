from fastapi import APIRouter

from app.api.routers.user import users

router = APIRouter()

router.include_router(users.router)