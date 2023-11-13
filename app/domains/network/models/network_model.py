from datetime import datetime
from pydantic import BaseModel


class PostInputSchema(BaseModel):
    title: str
    body_text: str


class ReplyInputSchema(BaseModel):
    body_text: str
    post_id: str


class NetWorkUserSchema(BaseModel):
    id: str
    name: str


class ReplyOutputSchema(BaseModel):
    id: str
    body_text: str
    user: NetWorkUserSchema
    date_created: datetime


class PostOutputSchema(BaseModel):
    id: str
    title: str
    body_text: str
    user: NetWorkUserSchema
    date_created: datetime


class DetailedPostOutputSchema(PostOutputSchema):
    replies: list[ReplyOutputSchema]
