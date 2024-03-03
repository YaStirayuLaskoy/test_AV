from pydantic import BaseModel


class FileEvent(BaseModel):
    path: str
