from fastapi import APIRouter, Depends, HTTPException,status,Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..  import database
from .. import models, pydantic_schemas, utils, oauth2

router = APIRouter(tags=["Authentication"])

# Generally if you want to send data in one direction we use POST method
# If you want to send data in both direction we use PUT method

@router.post("/login", status_code=status.HTTP_200_OK, response_model=pydantic_schemas.Token) # This is the login endpoin
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    utils.verify(user_credentials.password, user.password) # This will verify the password
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    # db: Session = Depends(get_db): Injects a SQLAlchemy session into the function so you can query the database.
    # user_credentials: A Pydantic model that contains the login info (likely a username/email and password).

    # Create and return token
    access_token = oauth2.create_access_token(data_payload={"user_id": user.id}) # data is payload
    # The payload is the data that you want to include in the token. In this case, we are including the user_id.
    return {"access_token": access_token, "token_type": "bearer"} # This is a fake token, you need to implement the token generation logic here