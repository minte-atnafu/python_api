from pydantic import BaseModel
from datetime import datetime
class PostBase(BaseModel):
    title: str
    content: str
    published: bool=True
    #we can also decalte optional porperties for post request
    # rating: Optional[int] = None


class CreatePost(PostBase):
    pass



class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mpde=True