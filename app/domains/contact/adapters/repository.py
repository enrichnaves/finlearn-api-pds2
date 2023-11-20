from fastapi import Depends
import sqlalchemy as sa
from sqlalchemy.orm import Session
from app.core.middleware.db import get_db
from app.domains.contact.domain.contact import Contact


class ContactRepository:
    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def create_contact(self, contact: Contact) -> None:
        self.db.add(contact)
        self.db.commit()

    def get_contacts(self) -> list[Contact]:
        stmt = sa.select(Contact)
        stmt_result = self.db.execute(stmt)
        return stmt_result.scalars().all()

    def get_by_id(self, id: str) -> Contact:
        stmt = sa.select(Contact).where(Contact.id == id)
        stmt_result = self.db.execute(stmt)
        return stmt_result.scalar()

    def get_by_email(self, email: str) -> Contact:
        stmt = sa.select(Contact).where(Contact.email == email)
        stmt_result = self.db.execute(stmt)
        return stmt_result.scalar()