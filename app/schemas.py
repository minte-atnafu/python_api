from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str
    published: bool=True
    #we can also decalte optional porperties for post request
    # rating: Optional[int] = None


class CreatePost(PostBase):
    pass