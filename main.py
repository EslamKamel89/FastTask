from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Path, status
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine  # type: ignore
from models import Todo, TodoCreate, TodoRead  # type: ignore

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally :
        db.close()


app = FastAPI()
db_dependency = Annotated[Session , Depends(get_db)]

@app.get('/')
async def home() :
    return {"message": "hello from FastAPI"}

@app.get('/todos' , status_code=status.HTTP_200_OK , response_model=list[TodoRead]) 
async def all_todos(db:db_dependency):
    return db.query(Todo).all()

@app.get('/todos/{todo_id}' , status_code=status.HTTP_200_OK , response_model=TodoRead)
async def get_todo(db:db_dependency , todo_id:Annotated[int , Path(ge=1 , description='todo id >= 1')]) : 
    todo = db.query(Todo).filter(Todo.id==todo_id).first()
    if todo is None :
        raise HTTPException(status_code=404 , detail=f"No todo with id: {todo_id} exist")
    return todo

@app.post('/todos' , response_model=TodoRead , status_code=status.HTTP_201_CREATED) 
async def create_todo(db:db_dependency, todo_request:TodoCreate) :
    todo = Todo(**todo_request.model_dump())
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

@app.put('/todos/{todo_id}' , response_model=TodoRead  , status_code=status.HTTP_201_CREATED) 
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

@app.delete('/todos/{todo_id}' , status_code=status.HTTP_204_NO_CONTENT)
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