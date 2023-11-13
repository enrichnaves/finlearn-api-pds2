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

@router.get("/posts", status_code=200, response_model=list[PostOutputSchema])
def get_posts(input:PracticeInputSchema):
  rate_value = 6 if input.rate == "CDB" else (8 if input.rate == 'TRUST_FUND" else 4.5
  investment = input.initial_investment
  monthly_rate = rate_value / 12 /100
  months = input.duration*12
  for _ in range(months):
    investment += input.monthly_investment
    investment*=(1+monthly_rate)

    return investment
