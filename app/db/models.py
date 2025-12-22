from sqlmodel import SQLModel, Field, Relationship 
from typing import Optional, List

class DBuser(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, nullable=False)
    email: str = Field(max_length=100, nullable=False, unique=True)
    hashed_password: str = Field(nullable=False)

    tasks: List["DBtask"] = Relationship(back_populates="owner")

class DBtask(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str = Field(max_length=100, nullable=False)
    description: Optional[str] = None
    completed: bool = Field(default=False, nullable=False)

    owner_id: Optional[int] = Field(default=None, foreign_key="users.id")
    owner: Optional["DBuser"] = Relationship(back_populates="tasks")