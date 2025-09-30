
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLITE:str = r"sqlite:///.\fast_task.db" 
POSTGRESQL:str=r"postgresql://postgres:password@localhost/todo"
SELECTED_DB : str = POSTGRESQL

engine = create_engine(SELECTED_DB , connect_args={'check_same_thread':False} if SELECTED_DB == SQLITE else {} ) # type: ignore

SessionLocal = sessionmaker(autocommit=False , autoflush=False , bind=engine)
Base = declarative_base()