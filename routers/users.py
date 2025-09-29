from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import SessionLocal
from models import User, UserRead
from security import CurrentUser, get_current_user

router = APIRouter(prefix='/users' , tags=['users'])
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session , Depends(get_db)]
user_dependency= Annotated[CurrentUser , Depends(get_current_user)]
bcrypt_context= CryptContext(schemes=['bcrypt'])

@router.get('/' , status_code=status.HTTP_200_OK , response_model=UserRead) 
async def get_user(
    user:user_dependency , 
    db: db_dependency , 
    ):
    user_model = db.query(User).filter(User.id == user.user_id).first()
    if user_model is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Authentication Failed")
    return user_model

class UserVerification(BaseModel) :
    password:str 
    new_password:str = Field(min_length=6)
@router.put('/password' , status_code=status.HTTP_204_NO_CONTENT) 
async def change_password(
    user: user_dependency , 
    db : db_dependency  , 
    body : UserVerification
    ) :
    user_model = db.query(User).filter(User.id == user.user_id ,).first()
    if user_model is None  or ( not bcrypt_context.verify(body.password , user_model.hashed_password)): # type: ignore
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Authentication Failed")
    user_model.hashed_password = bcrypt_context.hash(body.new_password) # type: ignore
    db.add(user_model)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)