

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel import select
from fastapi.security import OAuth2PasswordRequestForm
from blog.db.database import SessionDep
from blog.db import models
from .. import schemas
from ..repositories import authentication


router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", status_code=status.HTTP_200_OK)
def login(db: SessionDep, request: OAuth2PasswordRequestForm = Depends()):
    return authentication.login(request, db)



    
