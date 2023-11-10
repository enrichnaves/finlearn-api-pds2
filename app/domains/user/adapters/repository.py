from fastapi import Depends
import sqlalchemy as sa
from sqlalchemy.orm import Session
from app.core.middleware.db import get_db
from app.domains.user.domain.user import User


class UserRepository:
    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def create_user(self, user: User) -> None:
        self.db.add(user)
        self.db.commit()

    def update_user(self, user: User) -> None:
        stmt = (
            sa.update(User)
            .where(User.id == user.id)
            .values(
                name=user.name,
                cpf=user.cpf,
                email=user.email,
                telephone=user.telephone,
                coins_amount=user.coins_amount,
            )
        )
        self.db.execute(stmt)
        self.db.commit()

    def get_by_id(self, id: str) -> User:
        stmt = sa.select(User).where(User.id == id)
        stmt_result = self.db.execute(stmt)
        return stmt_result.scalar()

    def get_by_email(self, email: str) -> User:
        stmt = sa.select(User).where(User.email == email)
        stmt_result = self.db.execute(stmt)
        return stmt_result.scalar()
