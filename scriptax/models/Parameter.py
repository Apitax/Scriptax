from scriptax.models.Label import Label
from pydantic import BaseModel
from typing import Any, List


class Parameter(BaseModel):
    label: List[Label]
    required: bool = False
    value: Any = None
    strict_type: str = None
