from ..db.database import SessionDep
from .. import schemas
from ..db import models
from ..hashing import Hash
from fastapi import HTTPException, status
from sqlmodel import select

def create_user(request: schemas.User, db: SessionDep):
    new_user = models.Users(name=request.name, email=request.email, password=Hash.argon2(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def fetch_users(db: SessionDep):
    users = db.exec(select(models.Users)).all()
    return users

def fetch_user_by_id(id: int, db: SessionDep):
    user = db.get(models.Users, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} is not found")
    return user