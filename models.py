from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database import Base


# class Note(Base):
#     __tablename__ = "notes"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String)
#     completed = Column(Boolean)
#     date = Column(DateTime)

class User(Base):
    __tablename__="users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    # password = Column(String)
    date = Column(DateTime)
    hashed_password = Column(String, nullable=False)
# password — the plain password a user enters when registering or logging in.
# hashed_password — the protected representation you store in Neon.
