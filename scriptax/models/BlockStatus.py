from pydantic import BaseModel, Any


class BlockStatus(BaseModel):
    returned: bool = False
    result: Any = None

    continued: bool = False
    done: bool = False
