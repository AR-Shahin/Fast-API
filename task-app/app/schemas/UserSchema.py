from pydantic import BaseModel
from typing import Union

class UserSchema(BaseModel):
    name : str
    email : str
    password : str
    status : Union[bool,None] = None

        
        
class UserSchemaOut(BaseModel):
    name : str
    email : str
    status : Union[bool,None] = None
    
    class Config:
        orm_mode = True