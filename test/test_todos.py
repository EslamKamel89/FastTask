from test.utils import *
from typing import Any, Generator

from fastapi import status

from models import Todo


def test_read_all_authenticated(test_todo: Generator[Todo, Any, None]):
    response = client.get('/todos')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [  {
           'complete': False,
           'description': 'test description',
           'id': 1,
           'priority': 5,
           'title': 'test title',
       }]
    
def test_read_one_authenticated(test_todo: Generator[Todo]):
    response = client.get('/todos/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
           'id': 1,
           'title': 'test title',
           'description': 'test description',
           'priority': 5,
           'complete': False,
       }
def test_read_one_authenticated_not_found(test_todo:Generator[Todo]):
    response = client.get('/todos/2')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail" : 'No todo with id: 2 exist'}
    
def test_create_todo(test_todo:Generator[Todo]):
    request_data : dict[str , str|int] = {
        'id': 2,
        'title': 'test title 2',
        'description': 'test description 2',
        'priority': 4,
        'complete': False,
    }
    response = client.post('/todos' , json=request_data)
    assert response.status_code == status.HTTP_201_CREATED
    db = TestingSessionLocal()
    new_todo = db.query(Todo).filter(Todo.id == 2).first()
    assert new_todo.title == request_data.get('title') # type: ignore
    assert new_todo.description == request_data.get('description') # type: ignore
    assert new_todo.priority == request_data.get('priority') # type: ignore
    assert new_todo.complete == request_data.get('complete') # type: ignore
    
def test_update_todo(test_todo:Generator[Todo]) :
    request_data: dict[str , str|int] = {
           'title': 'test title updated',
           'description': 'test description updated',
           'priority': 3,
           'complete': True,
       }
    response = client.put('/todos/1' , json=request_data)
    assert response.status_code == status.HTTP_201_CREATED
    db = TestingSessionLocal()
    updated_todo = db.query(Todo).filter(Todo.id == 1).first()
    assert updated_todo.title == request_data.get('title') # type: ignore
    assert updated_todo.description == request_data.get('description') # type: ignore
    assert updated_todo.priority == request_data.get('priority') # type: ignore
    assert updated_todo.complete == request_data.get('complete') # type: ignore
    
def test_delete_todo(test_todo:Generator[Todo]) :
    response = client.delete('/todos/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    todos = db.query(Todo).all()
    assert todos == []
    