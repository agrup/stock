from fastapi import APIRouter
from src.app.api.v1.routes import users

router = APIRouter()

router.include_router(users.router)
