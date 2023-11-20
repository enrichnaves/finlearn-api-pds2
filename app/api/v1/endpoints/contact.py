from fastapi import APIRouter, Depends

from app.core.middleware.error_handler import ErrorModel

from app.core.models.api_aux import SuccessOperationSchema

from app.domains.user.adapters.repository import UserRepository
from app.providers import hash_provider
from app.domains.user.domain.user import User, UserRole
from app.domains.user.models.user_model import (
    UserInputSchema,
    UserOutputSchema,
    UserRolesEnum,
)


router = APIRouter()


@router.post("/create", status_code=201, response_model=SuccessOperationSchema)
def create_user(
    contact_input: ContactInputSchema,
    contact_repository: ContactRepository = Depends(ContactRepository),
):
    """
    Registra uma dúvida.

    - Acesso: ALL
    """

    contact = Contact(
        name=contact_input.name,
        email=contact_input.email,
        subject=contact_input.subject,
        doubt=contact_input.doubt,
    )


    contact_repository.create_contact(contact)

    return SuccessOperationSchema(success_detail="Usuário cadastrado com sucesso")