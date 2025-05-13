from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


# class Post(BaseModel): # Posts extends BaseModel
#     title: str
#     content: str
#     published: bool = False # User doesnt need to provide this field, it will be False by default

# class CreatePost(BaseModel):
#     title: str
#     content: str
#     published: bool = True

# class UpdatePost(BaseModel):
#     title: str
#     content: str
#     published: bool

# Direction of user sending data to the server
# User -> Request Body -> Pydantic Model -> Path Operation Function
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

# Shape of the model that we want to send to the user
# We dont want to send the password back to the user
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

# Direction of server sending data to the user
# Path Operation Function -> Pydantic Model -> Response Body -> User (Postman or UI)
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    
    class Config:
        orm_mode = True
# orm_mode = True is used to tell Pydantic to parse the SQLAlchemy model to a Pydantic model

class PostOut(BaseModel):
    post: Post  # NOT PostBase, and lowercase 'post' here
    votes: int

    class Config:
        from_attributes = True  # for Pydantic v2
        orm_mode = True
        
class UserCreate(BaseModel):
    email: EmailStr
    password: str



class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # dir can be 0 or 1, 0 means dislike and 1 means like
    # conint is used to create a constrained integer, le means less than or equal to 1
    # dir: conint(le=1) = 0 or 1, dir can be 0 or 1, 0 means dislike and 1 means like
