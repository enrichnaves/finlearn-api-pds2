from enum import Enum
from pydantic import BaseModel


class UserRolesEnum(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"

    def __str__(self):
        return str(self.value)


class UserInputSchema(BaseModel):
    email: str
    cpf: str
    name: str
    telephone: str
    password: str


class UserOutputSchema(BaseModel):
    id: str
    name: str
    cpf: str
    email: str
    telephone: str
    roles: list[UserRolesEnum]


class LoginSuccessSchema(BaseModel):
    user: UserOutputSchema
    access_token: str
