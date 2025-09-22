from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Todo, TodoCreate, TodoRead

router = APIRouter(prefix='/todos' , tags=['todos']) 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally :
        db.close()

db_dependency = Annotated[Session , Depends(get_db)]




@router.get('/' , status_code=status.HTTP_200_OK , response_model=list[TodoRead]) 
async def all_todos(db:db_dependency):
    return db.query(Todo).all()

@router.get('/{todo_id}' , status_code=status.HTTP_200_OK , response_model=TodoRead)
async def get_todo(db:db_dependency , todo_id:Annotated[int , Path(ge=1 , description='todo id >= 1')]) : 
    todo = db.query(Todo).filter(Todo.id==todo_id).first()
    if todo is None :
        raise HTTPException(status_code=404 , detail=f"No todo with id: {todo_id} exist")
    return todo

@router.post('/' , response_model=TodoRead , status_code=status.HTTP_201_CREATED) 
async def create_todo(db:db_dependency, todo_request:TodoCreate) :
    todo = Todo(**todo_request.model_dump())
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

@router.put('/{todo_id}' , response_model=TodoRead  , status_code=status.HTTP_201_CREATED) 
async def update_todo(
    db:db_dependency  , 
    todo_id :Annotated[int , Path(ge=1,description='todo id must be >= 1')] , 
    todo_request:TodoCreate
    ) :
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo_model is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f'No todo with this {id} exist')
    todo_model.title = todo_request.title # type: ignore
    todo_model.description = todo_request.description  # type: ignore
    todo_model.priority = todo_request.priority # type: ignore
    todo_model.complete = todo_request.complete # type: ignore
    db.add(todo_model)
    db.commit()
    return todo_model

@router.delete('/{todo_id}' , status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    db:db_dependency , 
    todo_id: Annotated[int , Path(ge=1 , description='todo id must be >= 1')]
    ):
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo_model is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"No todo with this id: {todo_id} exist")
    # db.query(Todo).filter(Todo.id == todo_id).delete() 
    db.delete(todo_model)
    db.commit()
    return 