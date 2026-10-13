from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base



# database models/table:
class Todo(Base):
    __tablename__ = "todos"  # table name

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    completed = Column(Boolean)

# creating relationships: connecting tables e.g:users and todos One to many relationship: one user can have many todos, aik table ka aik row multiple table ke rows ke sath connect hote hain, 
# to generate a relationship: use ForeignKey("tablename+idcolumnname")
#  ondelete="CASCADE": jab bhi koi user delete hoga uske andar todos delete honge, cascade means connect, now after this add alembic and all those changes written down there.
    user_id=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

# alembic: db migration tool, CLI->first: uv add alebmic, then: uv run alembic init migrations, then after this go into migrations folder and configure env.py  then after doing all the few config changes in env.py run: uv run alembic revision --autogenerate -m "add user_id to todos", then implement this in db running: uv run alembic upgrade head

# assigning specific todos to specific users after auth implemented, e.g: user1 has todo1, todo2 user2 has todo3, todo4, in main.py of todos we have to add user_id in the update operation 
# @app.post("/api/todos", response_model=schemas.Todo)
# def create_todos(
#     todo: schemas.TodoCreate,
#     db: Session = Depends(get_db),
#     user: User = Depends(get_current_user)
# ):
#     todos = models.Todo(
#         **todo.model_dump(),
#         user_id=user.id
#     )

#     db.add(todos)
#     db.commit()
#     db.refresh(todos)

#     return todos