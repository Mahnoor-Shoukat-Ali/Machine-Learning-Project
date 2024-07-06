from sqlmodel import SQLModel, Field
from typing import Optional

class TodoBase(SQLModel):
    title: str
    description: Optional[str] = None

class Todo(TodoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class TodoCreate(TodoBase):
    pass

class TodoRead(TodoBase):
    id: int
