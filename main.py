from fastapi import FastAPI, Depends, HTTPException
from database import engine, get_db
from sqlalchemy.orm import Session
from typing import List

from sqlalchemy.orm import Session
from database import get_db

from auth import bcrypt_context,create_token, verify_token
from database import get_db

app=FastAPI()

import models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# create users:  schemas.User
@app.post("/api/users", response_model=schemas.User)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
# Create a database user manually instead of using model_dump(), because the schema uses 'password' but the database uses 'hashed_password'
    # users = models.User(**user.model_dump())
    users=models.User(username=user.username,
                    email=user.email,
                    # Hash the plain password before storing it in the database
                    hashed_password=bcrypt_context.hash(user.password),
                    date=user.date)
    db.add(users)
    db.commit()
    db.refresh(users)
    return users


# get all users : List [schemas.User]
@app.get("/api/users", response_model=List[schemas.User])
def get_all_users(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users


# get single User: schemas.User
@app.get("/api/users/{user_id}", response_model=schemas.User)
def get_users(user_id: int, db: Session = Depends(get_db)): # Depends — tells FastAPI to run another function and provide its result.
    users = db.query(models.User).filter(models.User.id == user_id).first()
    return users


# update a User:
@app.put("/api/users/{user_id}", response_model=schemas.User)
def update_users(
    user_id: int,
    db: Session = Depends(get_db),
    updated_users: schemas.UserCreate = None,
):
    users = db.query(models.User).filter(models.User.id == user_id).first()
    if not users:
        raise HTTPException(status_code=404, detail="User not found")
    users.username = updated_users.username
    users.email = updated_users.email
    users.hashed_password=updated_users.hashed_password
    db.add(users)
    db.commit()
    db.refresh(users)
    return users


# delete a User:
@app.delete("/api/users/{user_id}", response_model=schemas.User)
def delete_users(
    user_id: int, 
    db: Session = Depends(get_db)):
    users = db.query(models.User).filter(models.User.id == user_id).first()
    if not users:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(users)
    db.commit()
    return users


# register: Create a new user account
@app.post("/api/register")
def register(user:schemas.User, db:Session=Depends(get_db)):
          # Check if a user with this username already exists
         existing_user=db.query(models.User).filter(models.User.username==user.username).first()
         # If a user exists, stop registration
         if  existing_user:
             raise HTTPException(status_code=400, detail="User already exists")
        # Hash the plain password entered by the user. Don't store the plain password in the database
         hashed_password=bcrypt_context.hash(user.password)
        # Create a new database user, 'password' is the input, 'hashed_password' is the database column
         new_user=models.User.insert().values(username= user.username, email=user.email, hashed_password=hashed_password, date=user.date)
         db.add(new_user)
         db.commit()
         db.refresh(new_user)
         return {"message":"User registered successfully"}


# Login: verify credentials and create a token
@app.post("/api/login")
def login(user: schemas.UserLogin, db:Session=Depends(get_db)):
    # Find a user matching the submitted username and email
    existing_user=db.query(models.User).filter(models.User.username==user.username, models.User.email==user.email).first()
    # If no matching user exists, reject the login
    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
     # Compare the entered plain password with the stored hash pass, bcrypt verifies the password, it does not decrypt the hash
    if not bcrypt_context.verify(user.password, existing_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid password")
    # If credentials are correct, generate an authentication token
    token=create_token({"username":user.username})
    return {"message":"Login successful", "token":token}


# Protected API(after verification access to api)
@app.get("/api/login/secure")   
def secureData(user= Depends(verify_token)):
    return {"message":f"Proctected data accessed by {user}"}
