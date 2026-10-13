from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Loads the environment variables from .env using load_dotenv
# Creates a SQLAlchemy engine using the database URL from the environment variables
# Creates a SessionLocal class for database sessions
# Defines a Base class for declarative models which will be used to create database tables
# Provides a get_db function to manage database connections
