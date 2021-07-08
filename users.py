#Response Model

from fastapi import FastAPI
from typing import List, Optional
from pydantic import BaseModel

app=FastAPI()


class User_in(BaseModel):
    username:str
    password:str
    email:str
    full_name:Optional[str]=None

class User_out(BaseModel):
    username:str
    email:str
    full_name:Optional[str]=None

@app.post("/user/",response_model=User_out)
def create_user(user:User_in):
    return user

