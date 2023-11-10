from pydantic import BaseModel


class SuccessOperationSchema(BaseModel):
    success_detail: str
