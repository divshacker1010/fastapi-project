from fastapi import FastAPI, Depends, status, Response, HTTPException
from typing import Annotated
from sqlmodel import Session, select
from . import schemas
from .hashing import Hash
from .db import models
from .db.database import create_db_and_tables, engine, get_session, SessionDep
# from passlib.context import CryptContext
# from pwdlib import PasswordHash
from .routers import blog, user


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# SessionDep = Annotated[Session, Depends(get_session)]

@app.get("/", tags=["Test"])
def read_root():
    return {"Home page, welcome to my blog API test project!"}

@app.get("/items/{item_id}",tags=["Test"])
def read_item(item_id: int, q: str | None=None):
    return {"item_id": item_id, "q": q}

# @app.get("/blog")
# def blog(limit=10,published: bool = True):
#     if published:
#         return {"list of published blogs": limit}
#     else:
#         return {"list of unpublished blogs": limit}

# @app.get("/blog", response_model=list[schemas.ShowBlog], tags=["Blogs"])
# def fetch_blog(db: SessionDep):
#     blogs = db.exec(select(models.Blog)).all()
#     return blogs
app.include_router(blog.router)
app.include_router(user.router)


# @app.get("/blog/published", tags=["Blogs"])
# def fetch_published(db: SessionDep):
#     blogs = db.exec(select(models.Blog).where(models.Blog.published == True)).all()
#     return blogs

# @app.get("/blog/unpublished", tags=["Blogs"])
# def fetch_unpublished(db: SessionDep):
#     blogs = db.exec(select(models.Blog).where(models.Blog.published == False)).all()
#     return blogs

# @app.get("/blog/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=["Blogs"])
# def blog_id(id: int, db: SessionDep, response: Response):
#     # blogs = db.exec(select(models.Blog).where(models.Blog.id == id)).first()
#     blogs = db.get(models.Blog, id)
#     if not blogs:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not found")
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {"message": f"Blog with the id {id} is not found"}
#     return blogs

# @app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["Blogs"])
# def update_blog(id: int, db: SessionDep, request: schemas.Blog):
#     blog = db.get(models.Blog, id)
#     if not blog:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not found")
#     blog.sqlmodel_update(request.dict(exclude_unset=True))
#     # blog.published = request.published or False
#     db.add(blog)
#     db.commit()
#     db.refresh(blog)
#     return f"Blog with id {id} is successfully updated"

# @app.post("/blog", status_code=status.HTTP_201_CREATED,tags=["Blogs"])
# def post_blog(request: schemas.Blog, db: SessionDep):
#     new_blog = models.Blog(title=request.title, body=request.body, published=request.published or False)
#     db.add(new_blog)
#     db.commit()
#     db.refresh(new_blog)
#     return new_blog
#     # return {"data": f"Blog is created with title as {request.title} and body as {request.body}"}

# @app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Blogs"])
# def delete_blog(id: int, db: SessionDep):
#     blog = db.get(models.Blog, id)
#     if not blog:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not found")
#     db.delete(blog)
#     db.commit()
#     return f"Blog with id {id} is successfully deleted"

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# @app.post("/user", status_code=status.HTTP_201_CREATED, tags=["Users"])
# def create_user(request: schemas.User, db: SessionDep):
#     # Encode password to bytes and truncate to 72 bytes (bcrypt limit)
#     # hashed_password = pwd_context.hash(request.password[:72])
#     new_user = models.Users(name=request.name, email=request.email, password=Hash.argon2(request.password))
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

# @app.get("/users", response_model=list[schemas.ShowUser], tags=["Users"])
# def fetch_users(db: SessionDep):
#     users = db.exec(select(models.Users)).all()
#     return users

# @app.get("/users/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowUser, tags=["Users"])
# def show_user(id: int, db: SessionDep):
#     user = db.get(models.Users, id)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} is not found")
#     return user

@app.get("/buildings", response_model=list[schemas.BuildingRead], tags=["Buildings"])
def fetch_buildings(db: SessionDep):
    buildings = db.exec(select(models.Building)).all()
    return buildings

@app.get("/owners", response_model=list[schemas.OwnerRead], tags=["Owners"])
def fetch_owners(db: SessionDep):
    owners = db.exec(select(models.Owner)).all()
    return owners

@app.get("/buildings/{id}", status_code=status.HTTP_200_OK, response_model=schemas.BuildingRead, tags=["Buildings"])
def show_building(id: int, db: SessionDep):
    building = db.get(models.Building, id)
    if not building:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Building with the id {id} is not found")
    return building

@app.get("/owners/{id}", status_code=status.HTTP_200_OK, response_model=schemas.OwnerRead, tags=["Owners"])
def show_owner(id: int, db: SessionDep):
    owner = db.get(models.Owner, id)
    if not owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Owner with the id {id} is not found")
    return owner

@app.post("/owner", status_code=status.HTTP_201_CREATED, tags=["Owners"])
def create_owner(request: schemas.OwnerCreate, db: SessionDep):
    new_owner = models.Owner(name=request.name, email=request.email)
    db.add(new_owner)
    db.commit()
    db.refresh(new_owner)
    return new_owner

@app.post("/building", status_code=status.HTTP_201_CREATED, tags=["Buildings"])
def create_building(request: schemas.BuildingCreate, db: SessionDep):
    new_building = models.Building(name=request.name, address=request.address, owner_id=request.owner_id)
    db.add(new_building)
    db.commit()
    db.refresh(new_building)
    return new_building

# @app.patch("/owner/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["Owners"])
# def update_owner(id: int, db: SessionDep, request: schemas.OwnerUpdate):
#     owner = db.get(models.Owner, id)
#     if not owner:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Owner with the id {id} is not found")
#     owner.sqlmodel_update(request.dict(exclude_unset=True))
#     db.add(owner)
#     db.commit()
#     db.refresh(owner)
#     return f"Owner with id {id} is successfully updated"

@app.patch("/building/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["Buildings"])
def update_building(id: int, db: SessionDep, request: schemas.BuildingUpdate):
    building = db.get(models.Building, id)
    if not building:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Building with the id {id} is not found")
    building.sqlmodel_update(request.dict(exclude_unset=True))
    db.add(building)
    db.commit()
    db.refresh(building)
    return f"Building with id {id} is successfully updated"