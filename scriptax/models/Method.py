from scriptax.models.Attributes import Attributes
from scriptax.models.Parameter import Parameter
from typing import List


class Method(Attributes):
    label: str
    parameters: List[Parameter]
