from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Response, status
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Todo, TodoRead
from security import CurrentUser, get_current_user

router = APIRouter(prefix='/admin' , tags=['admin']) 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally :
        db.close()

db_dependency = Annotated[Session , Depends(get_db)]

def admin_required(user: CurrentUser = Depends(get_current_user)) ->CurrentUser :
    if user.role != 'admin' :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin only")
    return user

admin_dependency = Annotated[CurrentUser, Depends(admin_required)]

@router.get('/todos' , status_code=status.HTTP_200_OK , response_model=list[TodoRead]) 
async def all_todos(
    admin: admin_dependency , 
    db: db_dependency , 
    ):  
    return db.query(Todo).all()

@router.delete('/todos/{todo_id}' , status_code=status.HTTP_204_NO_CONTENT )
async def delete_todo(
    admin : admin_dependency , 
    db: db_dependency , 
    todo_id : Annotated[int , Path(ge=1 , description='todo id must be >=1')]
    ):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail='Todo not found')
    db.delete(todo)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)