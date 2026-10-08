from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

#  BaseModel is the foundational class provided by Pydantic used for data validation, parsing, and settings management.
# • How it works: You create classes that inherit from BaseModel and define data fields using Python type annotations.
# • Validation: When data (such as JSON or untrusted API payloads) is passed to the model, Pydantic automatically validates, coerces, and parses the values to match your specified types4

# dict              → todo["id"]
# Todos object      → todo.id

app = FastAPI()

# using pydantic first validate the data
class Todos(BaseModel):
    id: int
    title: str
    description: str
    completed: bool


# create empty list for todos so that we can append data to it
todos = []


# create todos
@app.post("/api/todos")
def createTodos(todo: Todos):
    todos.append(todo)
    return {"message": "todo created successfully", "todos": todos}


# get all todos
@app.get("/api/todos")
def readTodos():
    return todos


# get one todo
@app.get("/api/todos/{todo_id}")
def getSingleTodo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return {"message": "todo found!", "todo": todo}
    raise HTTPException(status_code=404, detail="todo not found todo not found / does not exist")


# update one todo
@app.put("/api/todos/{todo_id}")
def updateTodo(todo_id: int, updated_todo: Todos):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[index] = updated_todo
            return {"message": "todo updated!", "todo": updated_todo}
        
    raise HTTPException(status_code=404, detail="todo not found todo not found / does not exist")
        


# delete one todo
@app.delete("/api/todos/{todo_id}")
def deleteTodo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(index)
            return {"message": f"todo {todo_id} deleted"}
    raise HTTPException(status_code=404, detail="todo not found / does not exist")
