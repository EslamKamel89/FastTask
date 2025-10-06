
from fastapi import APIRouter, HTTPException, Response, status
from pydantic import BaseModel, Field

from models import User, UserRead
from security import db_dependency, user_dependency

router = APIRouter(prefix='/users' , tags=['users'])


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
class PhoneRequest(BaseModel) :
    phone_number:str =Field(min_length=6 , max_length=20)
    
@router.put('/phone-number' , status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(
    user:user_dependency , 
    db : db_dependency , 
    body:PhoneRequest
):
    user_model = db.query(User).filter(User.id == user.user_id).first()
    if user_model is None: # type: ignore
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Authentication Failed")
    user_model.phone_number = body.phone_number # type: ignore
    db.add(user_model)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)