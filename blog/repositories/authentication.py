

from fastapi import  HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from datetime import timedelta
from blog.db.database import SessionDep

from blog.db import models
from .. import schemas
from ..hashing import Hash
# from ..schemas import Token, Login
from .token import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

def login(request: OAuth2PasswordRequestForm, db: SessionDep):
    new_user = db.exec(select(models.Users).where(models.Users.email == request.username)).first()
    if not new_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the email {request.username} is not found")
    if not Hash.verify(request.password, new_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.email}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")
