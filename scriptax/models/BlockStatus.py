from pydantic import BaseModel, Any


class BlockStatus(BaseModel):
    returned: bool
    result: Any

    continued: bool
    done: bool
