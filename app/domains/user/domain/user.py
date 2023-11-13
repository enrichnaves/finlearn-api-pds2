from typing import TYPE_CHECKING, Optional
from app.core.models.ddd_aux import ImplictDateTime, ImplictId


if TYPE_CHECKING:
    from app.domains.network.domain.network import (
        Post,
        Reply,
        PostValuation,
        ReplyValuation,
    )


class User:
    id: ImplictId
    date_created: ImplictDateTime
    date_updated: ImplictDateTime
    roles: Optional[list["UserRole"]]
    posts: list["Post"]
    replies: list["Reply"]
    posts_valuations: list["PostValuation"]
    replies_valuations: list["ReplyValuation"]

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
        self.roles = []
        self.posts = []
        self.replies = []

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

    def pay(self, amount: int, receiver_user: "User") -> None:
        if (self.coins_amount - amount) < 0:
            raise ValueError("Moedas insuficientes")
        receiver_user.coins_amount += amount
        self.coins_amount -= amount

    def valuate_post(self, post: "Post", is_up: bool) -> "PostValuation":
        if is_up:
            try:
                self.pay(amount=5, receiver_user=post.user)
            except ValueError as error:
                raise error
        valuation = PostValuation(is_up=is_up, user=self, post=post)
        self.posts_valuations.append(valuation)
        return valuation

    def valuate_reply(self, reply: "Reply", is_up: bool) -> "ReplyValuation":
        if is_up:
            try:
                self.pay(amount=5, receiver_user=reply.user)
            except ValueError as error:
                raise error
        valuation = ReplyValuation(is_up=is_up, user=self, reply=reply)
        self.replies_valuations.append(valuation)
        return valuation


class UserRole:
    id: ImplictId
    date_created: ImplictDateTime
    date_updated: ImplictDateTime

    def __init__(self, custom_role: str, user: User) -> None:
        self.custom_role = custom_role
