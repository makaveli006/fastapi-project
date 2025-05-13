
from fastapi import FastAPI, Body,Response,status,HTTPException, Depends
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, pydantic_schemas,utils
from .database import  engine,get_db
from sqlalchemy.orm import Session
from .routers import post, user, auth,vote



models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router) # This will include the post router
app.include_router(user.router) # We are grabbing the router object from the user file
app.include_router(auth.router) # We are grabbing the router object from the auth file
app.include_router(vote.router) # We are grabbing the router object from the vote file

@app.get("/")
async def root():
    return {"message": "Hello World"}





