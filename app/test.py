from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, pydantic_schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine) 

app = FastAPI()

@app.get("/posts", response_model=list[pydantic_schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).all()

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=pydantic_schemas.Post)
def create_post(post: pydantic_schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post  # Ensure we return only the post object

@app.get("/posts/{id}", response_model=pydantic_schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} is not found")
    return post  # Ensure direct return

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} is not found")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", response_model=pydantic_schemas.Post)
def update_post(id: int, updated_post: pydantic_schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} is not found")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()  # Ensure direct return
