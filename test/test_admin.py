from test.utils import *
from typing import Generator

from fastapi import status

from models import Todo


def test_admin_read_all_authenticated(test_todo: Generator[Todo]):
    response = client.get('/admin/todos')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        "id":1 ,
        "title":'test title' ,
        "description":'test description',
        "priority":5,
        "complete": False , 
    }]