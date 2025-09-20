from typing import Annotated  # type: ignore

from pydantic import BaseModel, ConfigDict, Field  # type: ignore
from sqlalchemy import Boolean, Column, Integer, String  # type: ignore

from database import Base


class Todo(Base) :
    __tablename__ = 'todos'
    id = Column(Integer , primary_key=True , index=True)
    title = Column(String(255))
    description = Column(String(255) , nullable=True)
    priority = Column(Integer)
    
class TodoBase(BaseModel):
    title:str 
    description:str |None = None
    priority:int 
    complete:bool = False 
class TodoRead(TodoBase) :
    id :int 
    model_config = ConfigDict(from_attributes=True)
class TodoCreate(TodoBase) :
    pass