from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Response, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Todo, TodoCreate, TodoRead

from .auth import CurrentUser, get_current_user

router = APIRouter(prefix='/admin' , tags=['admin']) 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally :
        db.close()

db_dependency = Annotated[Session , Depends(get_db)]

    
user_dependency = Annotated[CurrentUser, Depends(get_current_user)]

@router.get('/todos' , status_code=status.HTTP_200_OK , response_model=list[TodoRead]) 
async def all_todos(
    user: user_dependency , 
    db: db_dependency , 
    ):
    if user.role == 'admin':
        return db.query(Todo).all()
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Authentication Failed")

@router.delete('/todos/{todo_id}' , status_code=status.HTTP_204_NO_CONTENT )
async def delete_todo(
    user : user_dependency , 
    db: db_dependency , 
    todo_id : Annotated[int , Path(ge=1 , description='todo id must be >=1')]
    ):
    if user.role == 'admin' : 
        todo = db.query(Todo).filter(Todo.id == todo_id).first()
        if todo is None :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail='Todo not found')
        db.delete(todo)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail='You are not authorized')