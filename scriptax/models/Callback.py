from pydantic import BaseModel
from scriptax.models.Parameter import Parameter
from typing import List, Any
import uuid


class Callback(BaseModel):
    parameters: List[Parameter]
    block: Any
    name: str = str(uuid.uuid4()) + '_callback'
