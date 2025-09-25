from datetime import datetime, timedelta, timezone
from typing import Annotated, Any

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SessionLocal
from models import User, UserCreate, UserRead  # type: ignore

bcrypt_context = CryptContext(schemes=['bcrypt']  )

SECRET_KEY = "289901b501c0dd3321d9972705d6015777892668d71b7983d72f3926d00d0ab1"
ALGORITHM = "HS256"

router = APIRouter(prefix='/auth' , tags=['auth'])
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]

@router.post('/' , status_code=status.HTTP_201_CREATED , response_model=UserRead )
async def create_user(db:db_dependency , user_request:UserCreate) :
    user = User(
        username = user_request.username ,
        email = user_request.email ,
        first_name = user_request.first_name ,
        last_name = user_request.last_name ,
        is_active = True ,
        role = user_request.role ,
        hashed_password= bcrypt_context.hash(user_request.password)
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
        return 'Failed authentication'
    token = create_access_token(user.username , user.id , timedelta(minutes=20)) # type: ignore
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


def create_access_token(username:str , user_id:int , expires_delta:timedelta) -> str:
    encode : dict[str, Any] = {"sub":username , 'id':user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp' : expires})
    return jwt.encode(encode , SECRET_KEY , algorithm=ALGORITHM)


    