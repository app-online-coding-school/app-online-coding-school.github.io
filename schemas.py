from pydantic import BaseModel

#pydantic model
class Blog(BaseModel):
    title:str
    body:str


