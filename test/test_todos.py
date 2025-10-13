from typing import Any, Generator

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine, text
from sqlalchemy.orm import sessionmaker

from database import Base
from main import app
from models import Todo
from security import CurrentUser, get_current_user, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL , 
    connect_args={"check_same_thread":False} , 
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False , autoflush=False , bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user()->CurrentUser:
    return CurrentUser(username='eslam' , user_id=1 , role='admin')
        
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todo(
        title='test title' ,
        description='test description',
        priority=5,
        complete = False , 
        owner_id = 1
        )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection :
        connection.execute(text('Delete FROM todos'))
        connection.commit()

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