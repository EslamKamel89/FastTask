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