from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import models, schemas
from database import engine, get_db
from typing import List

# dict              → todo["id"]
# Todos object      → todo.id


# models — your file containing database models.
# Base — the foundation used to define your database tables.
# metadata — keeps information about those tables.
# create_all() — creates tables that don't exist yet.
# engine — the connection to your Neon database.
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# create todos in db
@app.post("/api/todos", response_model=schemas.Todo)
def create_todos(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    todos = models.Todo(**todo.model_dump())
    db.add(todos)
    db.commit()
    db.refresh(todos)
    return todos


# get all todos
@app.get("/api/todos", response_model=List[schemas.Todo])
def read_todos(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    todos = db.query(models.Todo).offset(skip).limit(limit).all()
    return todos


# get single todo
@app.get("/api/todos/{todo_id}", response_model=schemas.Todo)
def read_single_todo(todo_id: int, db: Session = Depends(get_db)):
    todos = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos


# update single todo
@app.put("/api/todos/{todo_id}", response_model=schemas.Todo)
def update_todos(
    todo_id: int, db: Session = Depends(get_db), updatedTask: schemas.TodoCreate = None
):
    todos = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    todos.title = updatedTask.title
    todos.description = updatedTask.description
    todos.completed = updatedTask.completed
    db.add(todos)
    db.commit()
    db.refresh(todos)
    return todos


@app.delete("/api/todos/{todo_id}", response_model=schemas.Todo)
def delete_todos(todo_id: int, db: Session = Depends(get_db)):
    todos = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todos)
    db.commit()
    return todos
