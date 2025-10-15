
import pytest
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
