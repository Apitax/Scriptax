from pydantic import BaseModel


class Range(BaseModel):
    start: int = 0
    stop: int = 0
    step: int = 1
