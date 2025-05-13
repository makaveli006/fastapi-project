from fastapi import FastAPI, Body,Response,status,HTTPException, Depends,APIRouter
from sqlalchemy.orm import Session
from ..import models, pydantic_schemas, utils
from ..database import  engine,get_db

router = APIRouter(prefix='/users',tags=['Users'])

# Creating users
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=pydantic_schemas.UserOut)
def create_user(user: pydantic_schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}",response_model=pydantic_schemas.UserOut)
def get_user(id :int,db: Session = Depends(get_db)):
    # First is used to get the first record that matches the query, without going through the entire table
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"User with id {id} is not found")
    return user