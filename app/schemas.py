from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool=True
    #we can also decalte optional porperties for post request
    # rating: Optional[int] = None


class CreatePost(PostBase):
    pass



class Post(BaseModel):
    id: int
    created_at: datetime

    class Config:
        orm_mpde=True

#defining user Schema

class PostUser(BaseModel):
    email: EmailStr
    password: str

class CreateUser(PostUser):
    pass    


class Users(BaseModel) :
    id: int   
    email:EmailStr


    class Config:
        orm_mpde=True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str   

class TokenData(BaseModel):
    id: Optional[str]
