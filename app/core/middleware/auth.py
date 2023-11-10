from fastapi import Depends

from fastapi.security import OAuth2PasswordBearer
from app.core.middleware.error_handler import ErrorModel
from app.domains.user.adapters.repository import UserRepository
from app.providers.token_provider import verify_acess_token
from jose import JWTError


oauth2_schema = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")


def _login(
    token: str = Depends(oauth2_schema),
    user_repository: UserRepository = Depends(UserRepository),
):
    try:
        user_id = verify_acess_token(token)
    except JWTError:
        raise ErrorModel.unauthorized(note="Token Inválido")

    if not user_id:
        raise ErrorModel.unauthorized(note="Token Inválido")

    user = user_repository.get_by_id(id=user_id)

    if not user:
        raise ErrorModel.unauthorized(note="Token Inválido")

    return user


def get_admin_user(
    token: str = Depends(oauth2_schema),
    user_repository: UserRepository = Depends(UserRepository),
):
    try:
        user = _login(token=token, user_repository=user_repository)
    except Exception:
        raise ErrorModel.unauthorized(note="Erro ao autenticar")

    if not user:
        raise ErrorModel.unauthorized(
            note="Erro ao autenticar, usuário não encontrado."
        )

    if not user.is_admin:
        raise ErrorModel.forbidden(note="Usuário não é Admin")

    return user


def get_user(
    token: str = Depends(oauth2_schema),
    user_repository: UserRepository = Depends(UserRepository),
):
    try:
        user = _login(token=token, user_repository=user_repository)
    except Exception:
        raise ErrorModel.unauthorized(note="Erro ao autenticar")

    if not user:
        raise ErrorModel.unauthorized(note="Erro ao logar, usuário não encontrado.")

    if not user.has_any_role:
        raise ErrorModel.forbidden(note="Usuário não é Admin")

    return user
