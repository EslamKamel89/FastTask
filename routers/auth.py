from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from models import User, UserCreate  # type: ignore

router = APIRouter(prefix='/auth' , tags=['auth'])
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]

@router.post('/' , )
async def create_user(db:db_dependency , user_request:UserCreate) :
    user = User(
        username = user_request.username ,
        email = user_request.email ,
        first_name = user_request.first_name ,
        last_name = user_request.last_name ,
        is_active = True ,
        role = user_request.role ,
        hashed_password= user_request.password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user