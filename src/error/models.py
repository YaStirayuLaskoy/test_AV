from pydantic import BaseModel


class ErrorQueueMessage(BaseModel):
    message: str
