from fastapi import FastAPI

import models
from database import Base, SessionLocal, engine  # type: ignore

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
@app.get('/')
async def home() :
    return {"message": "hello from FastAPI"}