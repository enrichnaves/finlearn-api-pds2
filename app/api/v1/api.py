from fastapi import APIRouter
from sqlalchemy.orm import configure_mappers
from app.domains.user.adapters.orm import start_mappers as user_start_mappers
from app.domains.network.adapters.orm import start_mappers as network_start_mappers
from app.domains.contact.adapters.orm import start_mappers as contact_start_mappers
from app.api.v1.endpoints import user, auth, network, contact

user_start_mappers()
network_start_mappers()
contact_start_mappers()
configure_mappers()


api_router = APIRouter()

api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(network.router, prefix="/network", tags=["network"])
api_router.include_router(contact.router, prefix="/contact", tags=["contact"])