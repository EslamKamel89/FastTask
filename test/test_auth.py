from datetime import timedelta
from test.utils import *
from typing import Generator

from fastapi import status
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
