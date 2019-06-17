from pydantic import BaseModel


class Attributes(BaseModel):
    script: bool = False
    static: bool = False
    asynchronous: bool = False
