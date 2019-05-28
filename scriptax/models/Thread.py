from pydantic import BaseModel
from scriptax.utilities.Threading import GenericExecution


class Thread(BaseModel):
    thread: GenericExecution
