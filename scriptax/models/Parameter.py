from pydantic import BaseModel
from typing import Any


class Parameter(BaseModel):
    name: str
    required: bool = False
    value: Any = None
    strict_type: str = None
