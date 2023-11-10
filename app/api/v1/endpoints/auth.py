from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.core.middleware.db import get_db
from app.core.middleware.error_handler import ErrorModel

from app.domains.user.domain.user import User
from app.domains.user.models.user_model import (
    LoginSuccessSchema,
    UserOutputSchema,
)
from app.domains.user.adapters.repository import UserRepository
from app.providers import hash_provider, token_provider
from app.core.middleware.auth import get_user


router = APIRouter()


@router.post("/login", response_model=LoginSuccessSchema)
def login(
    login_data: OAuth2PasswordRequestForm = Depends(),
    user_repository: UserRepository = Depends(UserRepository),
):
    """
    Rota para retornar um access_token.

    - Acesso: ALL
    """
    email = login_data.username
    password = login_data.password

    user = user_repository.get_by_email(email=email)

    if not user:
        raise ErrorModel.bad_request(note="Usuário ou senha estão incorretos!")

    valid_pass = hash_provider.verify_hash(password, user.password)

    if not valid_pass:
        raise ErrorModel.bad_request(note="Usuário ou senha estão incorretos!")

    token = token_provider.create_access_token({"sub": str(user.id)})

    user_schema = UserOutputSchema(
        id=str(user.id),
        name=user.name,
        cpf=user.cpf,
        email=user.email,
        telephone=user.telephone,
        roles=[role.custom_role for role in user.roles],
    )

    return LoginSuccessSchema(user=user_schema, access_token=token)


@router.get("/me", response_model=UserOutputSchema)
def get_me(current_user: User = Depends(get_user)):
    """
    Retorna informações do usuário autenticado.

    - Acesso: ALL
    """

    return UserOutputSchema(
        id=str(current_user.id),
        name=current_user.name,
        cpf=current_user.cpf,
        telephone=current_user.telephone,
        email=current_user.email,
        roles=[role.custom_role for role in current_user.roles],
    )
