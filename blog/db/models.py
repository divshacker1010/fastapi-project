# from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional


# class Hero(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     name: str = Field(index=True)
#     age: int | None = Field(default=None, index=True)
#     secret_name: str


class Blog(SQLModel, table=True):
    id: int |None = Field(default=None,primary_key=True, index=True)
    title: str = Field(unique=True)
    body: str
    published: bool = Field(default=True)

class Users(SQLModel, table=True):
    # model_config = {"table_name": "users"}
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True)
    password: str


class Owner(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True)
    buildings: list["Building"] = Relationship(back_populates="owner")

class Building(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    address: str
    owner_id: int|None = Field(foreign_key="owner.id")
    owner: Optional[Owner] = Relationship(back_populates="buildings") 

# app = FastAPI()


# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()


# @app.post("/heroes/")
# def create_hero(hero: Hero, session: SessionDep) -> Hero:
#     session.add(hero)
#     session.commit()
#     session.refresh(hero)
#     return hero


# @app.get("/heroes/")
# def read_heroes(
#     session: SessionDep,
#     offset: int = 0,
#     limit: Annotated[int, Query(le=100)] = 100,
# ) -> list[Hero]:
#     heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
#     return heroes


# @app.get("/heroes/{hero_id}")
# def read_hero(hero_id: int, session: SessionDep) -> Hero:
#     hero = session.get(Hero, hero_id)
#     if not hero:
#         raise HTTPException(status_code=404, detail="Hero not found")
#     return hero


# @app.delete("/heroes/{hero_id}")
# def delete_hero(hero_id: int, session: SessionDep):
#     hero = session.get(Hero, hero_id)
#     if not hero:
#         raise HTTPException(status_code=404, detail="Hero not found")
#     session.delete(hero)
#     session.commit()
#     return {"ok": True}