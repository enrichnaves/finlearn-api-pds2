from fastapi import Depends
import sqlalchemy as sa
from sqlalchemy.orm import Session
from app.core.middleware.db import get_db
from app.domains.network.domain.network import Post, Reply


class PostRepository:
    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def create_post(self, post: Post) -> None:
        self.db.add(post)
        self.db.commit()

    def get_posts(self) -> list[Post]:
        stmt = sa.select(Post)
        stmt_result = self.db.execute(stmt)
        return stmt_result.scalars().all()

    def get_by_id(self, id: str) -> Post:
        stmt = sa.select(Post).where(Post.id == id)
        stmt_result = self.db.execute(stmt)
        return stmt_result.scalar()


class ReplyRepository:
    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def create_reply(self, reply: Reply) -> None:
        self.db.add(reply)
        self.db.commit()

    def get_replies(self) -> list[Reply]:
        stmt = sa.select(Reply)
        stmt_result = self.db.execute(stmt)
        return stmt_result.scalars().all()

    def get_by_id(self, id: str) -> Reply:
        stmt = sa.select(Reply).where(Reply.id == id)
        stmt_result = self.db.execute(stmt)
        return stmt_result.scalar()
