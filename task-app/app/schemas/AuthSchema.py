from pydantic import BaseModel
from typing import Union

class LoginSchema(BaseModel):
    email : str
    password : Union[str,int]
    
    
class TokenData(BaseModel):
    email : str