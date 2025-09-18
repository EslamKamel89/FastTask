from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine  # type: ignore
from models import Todo

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

@app.get('/todos') 
async def all_todos(db:db_dependency) :
    return db.query(Todo).all()