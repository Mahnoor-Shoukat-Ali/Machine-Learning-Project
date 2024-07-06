from fastapi import FastAPI, HTTPException, Depends
from typing import List  # Import List from typing
from sqlmodel import Session, SQLModel, select  # Import SQLModel
from .models import Todo, TodoCreate, TodoRead
from .db import engine, get_session

app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.post("/todos/", response_model=TodoRead)
def create_todo(
    todo: TodoCreate, 
    session: Session = Depends(get_session)
):
    db_todo = Todo.from_orm(todo)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

@app.get("/todos/", response_model=List[TodoRead])
def read_todos(
    session: Session = Depends(get_session)
):
    todos = session.exec(select(Todo)).all()
    return todos

@app.delete("/todos/{todo_id}", response_model=TodoRead)
def delete_todo(
    todo_id: int, 
    session: Session = Depends(get_session)
):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    session.delete(todo)
    session.commit()
    return todo
