from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import pydantic_schemas,database,models,utils
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from .config import settings
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") # This is the url where we will send the token to get the user

# NEEDABLES
# 1. SECRET_KEY
# 2. ALGORITHM
# 3. ACCESS_TOKEN_EXPIRE_MINUTES

# SECRET_KEY = "d0ca8698g0-9df7g9fda0-5a48f09d9fbf87bc-11ef-9a7d-52540036dg6g8f8d9d980sdyfyohc8e"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60

SECRET_KEY = settings.secret_key # This is the secret key that will be used to encode the token
ALGORITHM = settings.algorithm # This is the algorithm that will be used to encode the token
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes # This is the time in minutes that the token will be valid for

def create_access_token(data_payload: dict):
    to_encode = data_payload.copy() # This is payload of the token
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id") # accessing the user_id from the payload
        # print(id)

        if id is None:
            raise credentials_exception
        token_data = pydantic_schemas.TokenData(id=id)
        # print(f"Token data: {token_data}")
    except JWTError:
        raise credentials_exception
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # This function will be used to get the current user from the token
    # It will decode the token and return the user id
    # It will also check if the token is valid or not
    # If the token is not valid it will raise an exception
    # If the token is valid it will return the user id
    # The user id will be used to get the user from the database
    # The user will be used to get the posts of the user
    # The posts will be used to get the comments of the user
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(token, credentials_exception)
    # print(f"Token: {token}")
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user