from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Response, status

from models import Todo, TodoRead
from security import admin_dependency, db_dependency

router = APIRouter(prefix='/admin' , tags=['admin']) 



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