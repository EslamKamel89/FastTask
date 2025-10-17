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
    
def test_admin_delete_todos(test_todo:Generator[Todo]) :
    response = client.delete('/admin/todos/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    todos = db.query(Todo).all()
    assert todos == []
    
def test_admin_delete_todos_not_fouond():
    response = client.delete('/admins/todo/2')
    assert response.status_code == status.HTTP_404_NOT_FOUND