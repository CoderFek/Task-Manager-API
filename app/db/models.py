from sqlmodel import SQLModel, Field
from typing import Optional

class DBtask(SQLModel, Table=True):
    id: int = Field(default=None, primary_key=True)
    title: str = Field(max_length=100, nullable=False)
    description: Optional[str] = None
    completed: bool = Field(default=False, nullable=False)