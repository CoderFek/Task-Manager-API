from sqlmodel import Session, create_engine, SQLModel
from app.db.models import DBuser, DBtask 

DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

def create_db_and_session():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session