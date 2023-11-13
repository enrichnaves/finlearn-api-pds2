from app.core.models.ddd_aux import ImplictDateTime, ImplictId
from app.domains.user.domain.user import User


class Post:
    id: ImplictId
    date_created: ImplictDateTime
    date_updated: ImplictDateTime
    replies: list["Reply"]
    valuations: list["PostValuation"]

    def __init__(self, title: str, body_text: str, user: User) -> None:
        self.title = title
        self.body_text = body_text
        self.user = user
        self.replies = []
        self.valuations = []

    @property
    def get_replies_by_relevance(self) -> list["Reply"]:
        sorted_replies = sorted(
            self.replies,
            key=lambda reply: sum(valuation.is_up for valuation in reply.valuations),
            reverse=True,
        )
        return sorted_replies


class Reply:
    id: ImplictId
    date_created: ImplictDateTime
    date_updated: ImplictDateTime
    valuations: list["ReplyValuation"]

    def __init__(self, body_text: str, user: User, post: Post) -> None:
        self.body_text = body_text
        self.user = user
        self.post = post
        self.valuations = []


class PostValuation:
    id: ImplictId
    date_created: ImplictDateTime
    date_updated: ImplictDateTime

    def __init__(self, is_up: bool, user: User, post: Post) -> None:
        self.is_up = is_up
        self.user = user
        self.post = post


class ReplyValuation:
    id: ImplictId
    date_created: ImplictDateTime
    date_updated: ImplictDateTime

    def __init__(self, is_up: bool, user: User, reply: Reply) -> None:
        self.is_up = is_up
        self.user = user
        self.reply = reply
