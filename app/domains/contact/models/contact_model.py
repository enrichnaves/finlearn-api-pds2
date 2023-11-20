from enum import Enum
from pydantic import BaseModel


class ContactInputSchema(BaseModel):
    name: str
    email: str
    subject: str
    doubt: str
