from fastapi import APIRouter, Depends, HTTPException, status, Response

from blog import schemas
from blog.db import models
from ..hashing import Hash
from ..db.database import SessionDep
from sqlmodel import Session, select
from ..repositories import user

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: SessionDep):
    # Encode password to bytes and truncate to 72 bytes (bcrypt limit)
    # hashed_password = pwd_context.hash(request.password[:72])
    # new_user = models.Users(name=request.name, email=request.email, password=Hash.argon2(request.password))
    # db.add(new_user)
    # db.commit()
    # db.refresh(new_user)
    # return new_user
    return user.create_user(request, db)

@router.get("/", response_model=list[schemas.ShowUser])
def fetch_users(db: SessionDep):
    return user.fetch_users(db)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def show_user(id: int, db: SessionDep):
    return user.fetch_user_by_id(id, db)