from app.core.models.ddd_aux import ImplictDateTime, ImplictId
from app.domains.user.models.user_model import UserRolesEnum


class User:
    id: ImplictId
    date_created: ImplictDateTime
    date_updated: ImplictDateTime
    roles: list["UserRole"]

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

    @property
    def is_admin(self) -> bool:
        for role in self.roles:
            if role.custom_role == "ADMIN":
                return True
        return False

    @property
    def has_any_role(self) -> bool:
        for role in self.roles:
            if role.custom_role:
                return True
        return False

    def has_this_role(self, _role: str) -> bool:
        for role in self.roles:
            if role.custom_role == _role:
                return True
        return False

    def add_role(self, role: "UserRole") -> None:
        if self.has_this_role(role.custom_role):
            raise ValueError("Usuário já possui a Role")
        else:
            self.roles.append(role)


class UserRole:
    id: ImplictId
    date_created: ImplictDateTime
    date_updated: ImplictDateTime

    def __init__(self, custom_role: str, user: User) -> None:
        self.custom_role = custom_role
