from typing import Annotated  # type: ignore

from pydantic import BaseModel, ConfigDict, Field  # type: ignore
from sqlalchemy import (Boolean, Column, ForeignKey, Integer,  # type: ignore
                        String)

from database import Base


class User(Base) :
    __tablename__ = 'users'
    id = Column(Integer , primary_key=True , index=True)
    username = Column(String ,unique=True, index=True)
    email = Column(String , unique=True , index=True)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    is_active = Column(Boolean , default=True)
    role = Column(String)

class UserBase(BaseModel) :
    username:str = Field(min_length=3 , max_length=255)
    email:str = Field(min_length=3 , max_length=255 )
    first_name:str = Field(min_length=3 , max_length=255)
    last_name:str = Field(min_length=3 , max_length=255)
    is_active:bool = False
    role:str = Field(min_length=3 , max_length=255)

class UserRead(UserBase) :
    id : int
    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase) :
    password:str = Field(min_length=3 , max_length=255)
    pass
class Todo(Base) :
    __tablename__ = 'todos'
    id = Column(Integer , primary_key=True , index=True)
    title = Column(String(255))
    description = Column(String(255) , nullable=True)
    priority = Column(Integer)
    complete = Column(Boolean , default=False)
    owner_id = Column(Integer, ForeignKey('users.id'))
class TodoBase(BaseModel):
    title:str = Field(min_length=3 , max_length=255)
    description:str |None = Field(None, min_length=3 , max_length=255 )
    priority:int = Field(ge=1 , le=5)
    complete:bool = False 
class TodoRead(TodoBase) :
    id :int 
    model_config = ConfigDict(from_attributes=True)
class TodoCreate(TodoBase) :
    pass