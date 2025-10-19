from test.utils import *
from typing import Generator

from fastapi import status

from models import Todo, User  # type: ignore
from routers.auth import authenticate_user


def test_authenticate_user(test_user: Generator[User]):
    db = TestingSessionLocal()
    user: User|bool = authenticate_user(test_user.username , 'password' , db) # type: ignore
    assert user != False
    assert user.username == test_user.username # type: ignore
    user = authenticate_user('eslam' , 'wrong' , db)
    assert user == False
    

