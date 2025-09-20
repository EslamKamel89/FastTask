from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Path, status
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine  # type: ignore
from models import Todo, TodoRead  # type: ignore

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

@app.get('/todos' , status_code=status.HTTP_200_OK) 
async def all_todos(db:db_dependency) :
    return db.query(Todo).all()

@app.get('/todos/{todo_id}' , status_code=status.HTTP_200_OK , response_model=TodoRead)
async def get_todo(db:db_dependency , todo_id:Annotated[int , Path(ge=1 , description='todo id >= 1')]) : 
    todo = db.query(Todo).filter(Todo.id==todo_id).first()
    if todo is None :
        raise HTTPException(status_code=404 , detail=f"No todo with id: {todo_id} exist")
    return todo