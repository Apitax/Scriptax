from pydantic import BaseModel
from scriptax.models.Parameter import Parameter
from scriptax.models.Label import Label
from typing import List, Any
import uuid


class Callback(BaseModel):
    parameters: List[Parameter]
    block: Any
    name: List[Label] = [Label(name=str(uuid.uuid4()) + '_callback')]
