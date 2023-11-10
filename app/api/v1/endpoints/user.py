from fastapi import APIRouter, Depends
from app.core.middleware.auth import get_admin_user

from app.core.middleware.error_handler import ErrorModel

from app.core.models.api_aux import SuccessOperationSchema

from app.domains.user.adapters.repository import UserRepository
from app.providers import hash_provider
from app.domains.user.domain.user import User, UserRole
from app.domains.user.models.user_model import UserInputSchema, UserRolesEnum


router = APIRouter()


@router.post("/create", status_code=201, response_model=SuccessOperationSchema)
def create_user(
    user_input: UserInputSchema,
    user_repository: UserRepository = Depends(UserRepository),
):
    """
    Registra um usuário.

    - Acesso: ALL
    """
    user_found = user_repository.get_by_email(email=user_input.email)

    if user_found:
        raise ErrorModel.bad_request("E-mail já cadastrado")

    user_input.password = hash_provider.generate_hash(user_input.password)

    user = User(
        name=user_input.name,
        email=user_input.email,
        cpf=user_input.cpf,
        password=user_input.password,
        telephone=user_input.telephone,
        coins_amount=50,
    )

    user_role = UserRole(custom_role="USER", user=user)

    try:
        user.add_role(user_role)
    except ValueError:
        raise ErrorModel.bad_request(note="Erro ao atribuir a Role")

    user_repository.create_user(user)

    return SuccessOperationSchema(success_detail="Usuário cadastrado com sucesso")


@router.post(
    "/add_role",
    status_code=201,
    response_model=SuccessOperationSchema,
)
def add_role(
    user_role: UserRolesEnum,
    user_id: str,
    user_repository: UserRepository = Depends(UserRepository),
    _current_user: User = Depends(get_admin_user),
):
    user = user_repository.get_by_id(user_id)

    if not user:
        return ErrorModel.not_found(note="Usuário não encontrado.")

    new_user_role = UserRole(custom_role=user_role, user=user)

    try:
        user.add_role(new_user_role)
    except ValueError:
        raise ErrorModel.bad_request(note=f"Usuário já possui a role: {user_role}")

    user_repository.update_user(user)

    return SuccessOperationSchema(success_detail="Role Adicionada")
