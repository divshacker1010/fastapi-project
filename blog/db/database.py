


# from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.params import Depends
from typing_extensions import Annotated

from sqlmodel import MetaData, Session, SQLModel, create_engine



# class Hero(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     name: str = Field(index=True)
#     age: int | None = Field(default=None, index=True)
#     secret_name: str

import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/blogdb"
)

engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    # print("metadata=",MetaData())
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)


# def get_session():
#     with Session(engine) as session:
#         yield session


# SessionDep = Annotated[Session, Depends(get_session)]