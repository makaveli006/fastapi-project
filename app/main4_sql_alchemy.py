
from fastapi import FastAPI, Body,Response,status,HTTPException, Depends
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, pydantic_schemas,utils
from .database import  engine,get_db
from sqlalchemy.orm import Session


# create_all() method is used to create the tables in the database
models.Base.metadata.create_all(bind=engine)    # This will create the tables in the database
# engine is used to connect to the database
# bind is used to bind the engine to the metadata
# In above how Base is used without importing it, because it is imported in the above line from . import models. Is it inherited from the models.py file?
# Base is a class that is defined in models.py file. It is inherited from the Base class in models.py file

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    # posts = db.query(models.Post) # This will return a query object, which is raw qury
    # print(posts)
    return {"data": posts}
    # return {"data": "success"}


@app.get("/posts",response_model=List[pydantic_schemas.Post])
# What is dependency injection?
# Dependency injection is a technique in which an object receives other objects that it depends on. These other objects are called dependencies.
# Why db: Session = Depends(get_db) is used?
# The get_db function returns a database session.
# What is Depends?
# Depends is a FastAPI function that allows you to include dependencies in your path operation functions.
# What is a dependency?
# A dependency is a function that provides the required data to the path operation function.
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts
    # return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED,response_model=pydantic_schemas.Post)
def create_post(post: pydantic_schemas.PostCreate, db: Session = Depends(get_db)): # This is path operation function
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published)) # This avoids SQL injection
    # new_post = cursor.fetchone()
    # conn.commit()
    # new_post = models.Post(title=post.title, content=post.content, published=post.published) # Creates a brand new post
    new_post = models.Post(**post.dict()) # Creates a brand new post, this is called dictionary unpacking
    # Why do we use **post.dict()? If we have large number of fields, we can use **post.dict() to avoid writing all the fields instead of writing all the fields like title=post.title, content=post.content, published=post.published
    # **post.dict() is used to convert the Pydantic model to a dictionary
    db.add(new_post) # We add the new post to the database session
    db.commit() # We commit the changes to the database
    db.refresh(new_post) # We refresh the new post to get the updated data
    return new_post
    # return {"data": new_post}


# Getting a single post
@app.get("/posts/{id}",response_model=pydantic_schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} is not found")
    return post
    # return {"post_detail": post}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} is not found")
    post.delete(synchronize_session=False)
    # synchronize_session=False is used to avoid the error: DetachedInstanceError: Instance <Post at 0x7f8b3c1b3d30> is not bound to a Session; attribute refresh operation cannot proceed
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}",response_model=pydantic_schemas.Post)
# The updated_post: Post parameter tells FastAPI that the request body should match the Post Pydantic model.
# FastAPI automatically extracts the data from the request body and converts it into a Post instance.
def update_post(id: int, updated_post: pydantic_schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)  # We setup a query to find the post with the given id
    post  = post_query.first() # We get the post with the given id
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} is not found")
    # post_query.update({'title': 'hey this is my updated title', 'content': 'this is my updated content'},synchronize_session=False)
    post_query.update(updated_post.dict(), synchronize_session=False)
    # updated_post.dict() is used to convert the Pydantic model to a dictionary
    # How pydantic model gets the user input?
    # Pydantic model gets the user input from the request body
    # I cant see anything specifying request body in the code, how does it get the user input?
    # Pydantic model gets the user input from the request body automatically
    # print(updated_post.dict())
    db.commit()
    return post_query.first()
    # return {"data": post_query.first()}


# Creating users
@app.post("/users", status_code=status.HTTP_201_CREATED,response_model=pydantic_schemas.UserOut)
def create_user(user: pydantic_schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users/{id}",response_model=pydantic_schemas.UserOut)
def get_user(id :int,db: Session = Depends(get_db)):
    # First is used to get the first record that matches the query, without going through the entire table
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"User with id {id} is not found")
    return user