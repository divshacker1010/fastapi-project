from urllib import request

from fastapi import APIRouter, Depends, HTTPException, status, Response

from blog import schemas
from blog.db import models
from ..db.database import SessionDep
from sqlmodel import Session, select
from ..repositories import blog

# from ..dependencies import get_token_header

router = APIRouter(
    prefix="/blog",
    tags=["Blogs"]
)

@router.get("/", response_model=list[schemas.ShowBlog])
def fetch_blog(db: SessionDep):
    return blog.get_all(db)

@router.get("/published")
def fetch_published(db: SessionDep):
    return blog.published(db)

@router.get("/unpublished")
def fetch_unpublished(db: SessionDep):
    return blog.unpublished(db)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def blog_id(id: int, db: SessionDep):
    # blogs = db.exec(select(models.Blog).where(models.Blog.id == id)).first()
    # blogs = blog.get_by_id(id, db)
    # if not blogs:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Blog with the id {id} is not found"}
    return blog.get_by_id(id, db)

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(id: int, db: SessionDep, request: schemas.Blog):
    return blog.put_by_id(id, db, request)
    # updated_blog = blog.put_by_id(id, db, request)
    # if not updated_blog:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not found")
    # return updated_blog

@router.post("/", status_code=status.HTTP_201_CREATED)
def post_blog(request: schemas.Blog, db: SessionDep):
    return blog.post_blog(request, db)
    # return new_blog
    

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: SessionDep):
    return blog.delete_blog(id, db)