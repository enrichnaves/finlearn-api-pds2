from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.middleware.db import get_db
from app.domains.user.domain.user import User


class UserRepository:
    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def create_user(self, user : User) -> None:
        self.db.add(user)
        self.db.commit()

    