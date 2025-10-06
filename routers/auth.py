from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from models import User, UserCreate, UserRead
from security import bcrypt_context, create_access_token, db_dependency

router = APIRouter(prefix='/auth' , tags=['auth'])

@router.post('/' , status_code=status.HTTP_201_CREATED , response_model=UserRead )
async def create_user(db:db_dependency , user_request:UserCreate) :
    user = User(
        username = user_request.username ,
        email = user_request.email ,
        first_name = user_request.first_name ,
        last_name = user_request.last_name ,
        is_active = True ,
        role = user_request.role ,
        hashed_password= bcrypt_context.hash(user_request.password) ,
        phone_number= user_request.phone_number,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

class Token(BaseModel) : 
    access_token:str 
    token_type:str

@router.post('/token'  , status_code=status.HTTP_200_OK , response_model=Token) 
async def login_for_access_token(
    db:db_dependency, 
    form_data:Annotated[OAuth2PasswordRequestForm , Depends()],):
    user = authenticate_user(form_data.username , form_data.password, db)
    if not user :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="could not validate user")
    token = create_access_token(user.username , user.id , user.role , timedelta(minutes=20)) # type: ignore
    return {
        "access_token" : token , 
        "token_type" : "bearer"
    }

def authenticate_user(username:str , password:str , db:Session):
    user = db.query(User).filter(User.username == username).first()
    if user is None :
        return False 
    if not bcrypt_context.verify(password , user.hashed_password) : # type: ignore
        return False 
    return user




    

    