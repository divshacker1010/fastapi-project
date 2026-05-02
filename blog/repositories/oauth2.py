from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from fastapi import Depends, FastAPI, HTTPException, status
from .token import verify_token
from typing import Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") # route from where fastapi uses to fetch token from to authenticate routes

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception)