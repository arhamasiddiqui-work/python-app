from pydantic import BaseModel

#  BaseModel is the foundational class provided by Pydantic used for data validation, parsing, and settings management.
# • How it works: You create classes that inherit from BaseModel and define data fields using Python type annotations.
# • Validation: When data (such as JSON or untrusted API payloads) is passed to the model, Pydantic automatically validates, coerces, and parses the values to match your specified types4

class TodoBase(BaseModel):
    title: str
    description: str
    completed: bool

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: int

    class Config:
        orm_mode = True





