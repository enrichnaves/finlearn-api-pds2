from fastapi import APIRouter, Depends

from app.core.middleware.error_handler import ErrorModel

from app.core.models.api_aux import SuccessOperationSchema

from app.domains.contact.adapters.repository import ContactRepository
from app.providers import hash_provider
from app.domains.contact.domain.contact import Contact
from app.domains.contact.models.contact_model import (
    ContactInputSchema,
)


router = APIRouter()


@router.post("/create", status_code=201, response_model=SuccessOperationSchema)
def create_contact(
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

    return SuccessOperationSchema(success_detail="Dúvida cadastrado com sucesso")
