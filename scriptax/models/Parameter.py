from pydantic import BaseModel
from typing import Any


class Parameter(BaseModel):
    name: str
    value: Any = None
