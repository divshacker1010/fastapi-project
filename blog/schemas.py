from pydantic import BaseModel
from typing import Optional

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]

class ShowBlog(BaseModel):
    title: str
    body: str
    class Config:
        orm_mode = True

class User(BaseModel):
    name: str
    email: str
    password: str

class ShowUser(BaseModel):
    name: str
    email: str
    id: int
    class Config:
        orm_mode = True

# Owner Schemas
class OwnerCreate(BaseModel):
    name: str
    email: str


class BuildingCreate(BaseModel):
    name: str
    address: str
    owner_id: int

class BuildingList(BaseModel):
    name: str
    address: str
    # owner_id: int

class OwnerList(BaseModel):
    # id: int
    name: str
    email: str


class OwnerRead(BaseModel):
    id: int
    name: str
    email: str
    buildings: list["BuildingList"] = []
    class Config:
        orm_mode = True

# Building Schemas

class BuildingRead(BaseModel):
    id: int
    name: str
    address: str
    owner: Optional["OwnerList"] = None
    class Config:
        orm_mode = True

class BuildingUpdate(BaseModel):
    # id: int
    name: Optional[str] = None
    address: Optional[str] = None
    owner_id: Optional[int] = None

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None

# class OwnerUpdate(BaseModel):
#     name: Optional[str]
#     email: Optional[str]
#     buildings: Optional[list["BuildingList"]] = []

# Update forward references
OwnerRead.model_rebuild()
BuildingRead.model_rebuild()