from typing import TYPE_CHECKING, Optional
from app.core.models.ddd_aux import ImplictDateTime, ImplictId


class Contact:
    id: ImplictId
    date_created: ImplictDateTime

    def __init__(
        self,
        name: str,
        email: str,
        subject: str,
        doubt: str,
    ) -> None:
        self.name = name
        self.email = email
        self.subject = subject
        self.doubt = doubt