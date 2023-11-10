from fastapi import APIRouter
from sqlalchemy.orm import configure_mappers
from app.domains.user.adapters.orm import start_mappers as user_start_mappers
from app.api.v1.endpoints import user, auth

user_start_mappers()
configure_mappers()


api_router = APIRouter()

api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
