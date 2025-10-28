from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Response, status
from sqlalchemy.exc import SQLAlchemyError

from models import Todo, TodoCreate, TodoRead
from security import db_dependency, user_dependency

router = APIRouter(prefix='/todos' , tags=['todos']) 

@router.get('/todo-page')
async def render_todos_page():
    return {'message':"hello world"}

@router.get('/' , status_code=status.HTTP_200_OK , response_model=list[TodoRead]) 
async def all_todos(user: user_dependency , db:db_dependency):
    if user is None : # type: ignore
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail='Authentication failed')
    todos = db.query(Todo).where(Todo.owner_id == user.user_id).all()
    return todos

@router.get('/{todo_id}' , status_code=status.HTTP_200_OK , response_model=TodoRead)
async def get_todo(user:user_dependency ,  db:db_dependency , todo_id:Annotated[int , Path(ge=1 , description='todo id >= 1')]) : 
    if user is None : # type: ignore
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail='Authentication failed')
    todo = db.query(Todo).filter(Todo.id==todo_id)\
            .filter(Todo.owner_id == user.user_id).first()
    if todo is None :
        raise HTTPException(status_code=404 , detail=f"No todo with id: {todo_id} exist")
    return todo

@router.post('/' , response_model=TodoRead , status_code=status.HTTP_201_CREATED) 
async def create_todo(user : user_dependency ,  db:db_dependency, todo_request:TodoCreate) :
    if user is None : # type: ignore
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail='Authentication failed')
    todo = Todo(**todo_request.model_dump() , owner_id=user.user_id)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

@router.put('/{todo_id}' , response_model=TodoRead  , status_code=status.HTTP_201_CREATED) 
async def update_todo(
    user:user_dependency , 
    db:db_dependency  , 
    todo_id :Annotated[int , Path(ge=1,description='todo id must be >= 1')] , 
    todo_request:TodoCreate
    ) :
    todo_model = db.query(Todo).filter(Todo.id == todo_id , Todo.owner_id == user.user_id ).first()
    if todo_model is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f'No todo with this {todo_id} exist')
    for key ,value in todo_request.model_dump().items() :
        setattr(todo_model , key , value)
    db.add(todo_model)
    db.commit()
    return todo_model

@router.delete('/{todo_id}' ,
               status_code=status.HTTP_204_NO_CONTENT ,
               summary='Delete a todo you own')
async def delete_todo(
    user: user_dependency , 
    db:db_dependency , 
    todo_id: Annotated[int , Path(ge=1 , description='todo id must be >= 1')]
    ):
    todo_model = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user.user_id).first()
    if todo_model is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"No todo with this id: {todo_id} exist")
    try:
        db.delete(todo_model)
        db.commit()
    except  SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR , detail=f"Could not delete todo")
    return Response(status_code=status.HTTP_204_NO_CONTENT)