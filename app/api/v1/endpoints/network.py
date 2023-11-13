from fastapi import APIRouter, Depends
from app.core.middleware.auth import get_user

from app.core.middleware.error_handler import ErrorModel

from app.core.models.api_aux import SuccessOperationSchema

from app.domains.network.adapters.repository import PostRepository, ReplyRepository
from app.domains.network.models.network_model import (
    DetailedPostOutputSchema,
    PostInputSchema,
    PostOutputSchema,
    NetWorkUserSchema,
    ReplyInputSchema,
    ReplyOutputSchema,
)
from app.domains.user.adapters.repository import UserRepository
from app.domains.network.domain.network import (
    Reply,
    Post,
    ReplyValuation,
    PostValuation,
)
from app.domains.user.domain.user import User


router = APIRouter()


@router.post("/create-post", status_code=201, response_model=SuccessOperationSchema)
def create_user(
    post_input: PostInputSchema,
    post_repository: PostRepository = Depends(PostRepository),
    user_repository: UserRepository = Depends(UserRepository),
    current_user: User = Depends(get_user),
):
    post = Post(
        title=post_input.title, body_text=post_input.body_text, user=current_user
    )
    post_repository.create_post(post)

    return SuccessOperationSchema(success_detail="Post cadastrado com sucesso")


@router.post("/create-reply", status_code=201, response_model=SuccessOperationSchema)
def create_reply(
    reply_input: ReplyInputSchema,
    post_repository: PostRepository = Depends(PostRepository),
    reply_repository: ReplyRepository = Depends(ReplyRepository),
    user_repository: UserRepository = Depends(UserRepository),
    current_user: User = Depends(get_user),
):
    post = post_repository.get_by_id(reply_input.post_id)
    if not post:
        raise ErrorModel.not_found("post não encontrado")

    reply = Reply(body_text=reply_input.body_text, user=current_user, post=post)
    reply_repository.create_reply(reply)

    return SuccessOperationSchema(success_detail="Reply cadastrada com sucesso")


@router.get("/posts", status_code=200, response_model=list[PostOutputSchema])
def get_posts(
    post_repository: PostRepository = Depends(PostRepository),
    _current_user: User = Depends(get_user),
):
    posts = post_repository.get_posts()

    return [
        PostOutputSchema(
            id=str(post.id),
            title=post.title,
            body_text=post.body_text,
            user=NetWorkUserSchema(id=str(post.user.id), name=post.user.name),
            date_created=post.date_created,
        )
        for post in posts
    ]


@router.get("/post/{post_id}", status_code=200, response_model=DetailedPostOutputSchema)
def get_post_by_id(
    post_id: str,
    post_repository: PostRepository = Depends(PostRepository),
    _current_user: User = Depends(get_user),
):
    post = post_repository.get_by_id(post_id)

    if not post:
        raise ErrorModel.not_found("post não encontrado")

    order_replies = post.get_replies_by_relevance

    return DetailedPostOutputSchema(
        id=str(post.id),
        title=post.title,
        body_text=post.body_text,
        user=NetWorkUserSchema(id=str(post.user.id), name=post.user.name),
        date_created=post.date_created,
        replies=[
            ReplyOutputSchema(
                id=str(reply.id),
                body_text=reply.body_text,
                date_created=reply.date_created,
                user=NetWorkUserSchema(id=str(reply.user.id), name=reply.user.name),
            )
            for reply in order_replies
        ],
    )
