from test.utils import *
from typing import Generator

from fastapi import status

from models import Todo  # type: ignore


def test_return_user(test_user:Generator[User]):
    response = client.get('/users')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == 1
    assert response.json()['username'] == 'eslam'
    assert response.json()['email'] ==  'admin@gmail.com'
    assert response.json()['first_name'] == 'eslam'
    assert response.json()['last_name'] == 'kamel'
    assert response.json()['is_active'] ==  True
    assert response.json()['role'] ==  'admin'
    assert response.json()['phone_number'] == '01020504470'
    
def test_change_password_success(test_user: Generator[User]):
    body:dict[str, str] = {'password':'password' , 'new_password':'updated'}
    response = client.put('/users/password' , json=body)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    user = db.query(User).filter(User.id == 1).first()
    assert user is not None
    assert bcrypt_context.verify('updated' , user.hashed_password) # type: ignore


def test_change_password_invalid(test_user:Generator[User]):
    body:dict[str, str] = {'password':'wrong' , 'new_password':'updated'}
    response = client.put('/users/password' , json=body)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
def test_phone_number_change(test_user:Generator[User]):
    body:dict[str,str] = {"phone_number" : "123456789"}
    response = client.put('/users/phone-number' , json=body)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    user = db.query(User).filter(User.id == 1).first()
    assert user is not None
    assert user.phone_number == body.get('phone_number') # type: ignore