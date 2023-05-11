from pydantic import BaseModel
from typing import Union

class TaskSchema(BaseModel):
    title : str
    description : Union[str,None] = None
    duration : Union[int,float]
    status : Union[bool,None] = None
    user_id : int