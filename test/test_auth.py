from datetime import datetime, timedelta
from test.utils import *
from typing import Any, Generator

import pytest
from fastapi import HTTPException, status  # type: ignore
from jose import jwt

from models import Todo, User  # type: ignore
from routers.auth import authenticate_user
from security import ALGORITHM, SECRET_KEY, create_access_token


def test_authenticate_user(test_user: Generator[User]):
    db = TestingSessionLocal()
    user: User|bool = authenticate_user(test_user.username , 'password' , db) # type: ignore
    assert user != False
    assert user.username == test_user.username # type: ignore
    user = authenticate_user('eslam' , 'wrong' , db)
    assert user == False
    
def test_create_access_token(test_user:Generator[User]) : 
    token = create_access_token(test_user.username , test_user.id , test_user.role , timedelta(days=1) ) # type: ignore
    assert token != '' 
    payload = jwt.decode(token , SECRET_KEY , algorithms=[ALGORITHM])
    assert test_user.username == payload.get('sub') # type: ignore
    assert test_user.id == payload.get('id') # type: ignore
    assert test_user.role == payload.get('role') # type: ignore


@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode: dict[str, Any] = {"sub":'eslam' ,'id':1 , 'role':'admin' , "exp" : datetime.now() + timedelta(days=1) }
    token:str = jwt.encode(encode , SECRET_KEY ,algorithm= ALGORITHM)
    user = await get_current_user(token)
    assert user.user_id == 1
    assert user.username == 'eslam'
    assert user.role == 'admin' 

@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode:dict[str ,Any] = {'role':'user'}
    token:str = jwt.encode(encode , SECRET_KEY , algorithm= ALGORITHM)
    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token)
    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED    