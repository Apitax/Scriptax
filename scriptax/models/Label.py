from pydantic import BaseModel


class Label(BaseModel):
    name: str = None
    start: int = None
    stop: int = None
