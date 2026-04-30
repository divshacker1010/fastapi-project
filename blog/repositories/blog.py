from sqlmodel import select
from fastapi import HTTPException, status
from blog.db import models
from ..db.database import SessionDep
from .. import schemas


def get_all(db: SessionDep):
    # return db.get(models.Blog)
    return db.exec(select(models.Blog)).all()

def published(db: SessionDep):
    return db.exec(select(models.Blog).where(models.Blog.published == True)).all()
    

def unpublished(db: SessionDep):
    return db.exec(select(models.Blog).where(models.Blog.published == False)).all()

def get_by_id(id: int, db: SessionDep):
    blog = db.get(models.Blog, id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not found")
    return blog

def put_by_id(id: int, db: SessionDep, request: schemas.Blog):
    blog = db.get(models.Blog, id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not found")
    blog.sqlmodel_update(request.dict(exclude_unset=True))
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog

def post_blog(request: schemas.Blog, db: SessionDep):
    new_blog = models.Blog(title=request.title, body=request.body, published=request.published or False)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {"data": f"Blog is created with title as {request.title} and body as {request.body}"}

def delete_blog(id: int, db: SessionDep):
    blog = db.get(models.Blog, id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not found")
    db.delete(blog)
    db.commit()
    return f"Blog with id {id} is successfully deleted"