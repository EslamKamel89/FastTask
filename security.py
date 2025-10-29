from datetime import datetime, timedelta, timezone
from typing import Annotated, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from database import SessionLocal

SECRET_KEY = "289901b501c0dd3321d9972705d6015777892668d71b7983d72f3926d00d0ab1"
ALGORITHM = "HS256"
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/auth/token')

class CurrentUser(BaseModel):
    username:str 
    user_id:int
    role:str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
async def get_current_user(token : Annotated[str , Depends(oauth2_bearer)]) ->CurrentUser : 
    try:
        payload = jwt.decode(token , SECRET_KEY , algorithms=[ALGORITHM])
        username:str|None = payload.get('sub')
        user_id:int|None = payload.get('id')
        role:str|None = payload.get('role')
        if username is None or user_id is None or role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="could not validate user")
        return CurrentUser(username=username , user_id=user_id , role= role)
    except JWTError as e: # type: ignore
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="could not validate user")

def create_access_token(username:str , user_id:int , role:str , expires_delta:timedelta) -> str:
    encode : dict[str, Any] = {"sub":username , 'id':user_id , "role":role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp' : expires})
    return jwt.encode(encode , SECRET_KEY , algorithm=ALGORITHM)

def admin_required(user: CurrentUser = Depends(get_current_user)) ->CurrentUser :
    if user.role != 'admin' :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin only")
    return user


db_dependency = Annotated[Session , Depends(get_db)]
user_dependency= Annotated[CurrentUser , Depends(get_current_user)]
bcrypt_context= CryptContext(schemes=['bcrypt'])
admin_dependency = Annotated[CurrentUser, Depends(admin_required)]

def redirect_to_login()->RedirectResponse:
    redirect_response = RedirectResponse('/auth/login-page')
    redirect_response.delete_cookie('access_token')
    return redirect_response