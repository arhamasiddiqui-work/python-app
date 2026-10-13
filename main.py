from fastapi import FastAPI, Depends, HTTPException
from database import engine, get_db
from sqlalchemy.orm import Session
from typing import List


import models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# create users:  schemas.User
@app.post("/api/users", response_model=schemas.User)
def create_users(User: schemas.UserCreate, db: Session = Depends(get_db)):
    users = models.User(**User.model_dump())
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
def get_users(user_id: int, db: Session = Depends(get_db)):
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
        raise HTTPException(stats_code=404, detail="User not found")
    users.title = updated_users.title
    users.description = updated_users.description
    users.completed = updated_users.completed
    db.add(users)
    db.commit()
    db.refresh(users)
    return users


# delete a User:
@app.delete("/api/users/{user_id}", response_model=schemas.User)
def delete_users(user_id: int, db: Session = Depends(get_db)):
    users = db.query(models.User).filter(models.User.id == user_id).first()
    if not users:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(users)
    db.commit()
    return {"message": "users deleted successfully", "User": users}
