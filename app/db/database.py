from typing import Generator
from sqlmodel import Session, create_engine, SQLModel
from app.db.models import DBtask

DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thred": False})

def create_db_and_session():
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """This manages the transaction lifecycle for each API request."""
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
    