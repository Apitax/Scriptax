from pydantic import BaseModel
from typing import List


class AhOptions(BaseModel):
    name: str = ""
    help: str = ""
    summary: str = ""
    description: str = ""
    author: str = ""
    version: str = ""
    link: str = ""
    available: bool = True
    enabled: bool = True
    access: List[str] = []
