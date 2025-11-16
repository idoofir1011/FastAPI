from pydantic import BaseModel, EmailStr
from typing import Optional, Literal


# -----------------
# Models
# -----------------


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    model_config = {"from_attributes": True}


class PostOut(PostBase):
    id: int
    owner_id: int
    owner: UserOut


class PostWithVotes(BaseModel):
    Post: PostOut
    votes: int
    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]
