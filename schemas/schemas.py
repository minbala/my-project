from datetime import datetime
from tkinter.tix import Tree
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserIn(BaseModel):
    email:EmailStr
    password:str
    
class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime

    
    class Config:
        orm_mode =True
        
class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str] =None
    
class PageBase(BaseModel):
    title:str
    content:str

class PageCreate(PageBase):
    pass
    
class PageOut(PageBase):
    id : int
    created_at:datetime
    owner_id:int
    owner:UserOut
    
    class Config:
        orm_mode=True
    