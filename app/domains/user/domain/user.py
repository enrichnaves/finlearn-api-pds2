from app.core.models.ddd_aux import ImplictDateTime, ImplictId


class User:
    id: ImplictId
    date_created: ImplictDateTime
    date_updated: ImplictDateTime

    def __init__(
        self,
        name: str,
        email: str,
        cpf: str,
        password: str,
        telephone: str,
        coins_amount: int,
    ) -> None:
        self.name = name
        self.email = email
        self.cpf = cpf
        self.password = password
        self.telephone = telephone
        self.coins_amount = coins_amount

   


class UserRole:
    id: ImplictId
    date_created: ImplictDateTime
    date_updated: ImplictDateTime

    def __init__(self, custom_role: str, user: User) -> None:
        self.custom_role = custom_role
