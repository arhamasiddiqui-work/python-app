from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base

# database models/table:
class Todo(Base):
    __tablename__="todos"   #table name

    id= Column(Integer, primary_key=True, index=True)
    title=Column(String)
    description=Column(String)
    completed=Column(Boolean)

