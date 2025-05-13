from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from .. import models, pydantic_schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[pydantic_schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""
):
    rows = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
          .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
          .group_by(models.Post.id)
          .filter(models.Post.title.contains(search))
          .limit(limit)
          .offset(skip)
          .all()
    )
    return [{"post": post, "votes": votes} for post, votes in rows]


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=pydantic_schemas.Post)
def create_posts(
    post: pydantic_schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=pydantic_schemas.PostOut)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    row = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
          .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
          .group_by(models.Post.id)
          .filter(models.Post.id == id)
          .first()
    )

    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )

    post_obj, votes = row
    return {"post": post_obj, "votes": votes}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=pydantic_schemas.Post)
def update_post(
    id: int,
    updated_post: pydantic_schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
