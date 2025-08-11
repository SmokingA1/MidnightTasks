from fastapi import APIRouter

from app.api.routers.user import users
from app.api.routers.user import login
from app.api.routers.project import projects
from app.api.routers.board import boards

router = APIRouter()

router.include_router(users.router)
router.include_router(login.router)
router.include_router(projects.router)
router.include_router(boards.router)