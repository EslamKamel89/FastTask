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
           'complete': False,
           'description': 'test description',
           'id': 1,
           'priority': 5,
           'title': 'test title',
       }
def test_read_one_authenticated_not_found(test_todo:Generator[Todo]):
    response = client.get('/todos/2')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail" : 'No todo with id: 2 exist'}