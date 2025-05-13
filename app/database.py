from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import settings
# Create a connection to the database
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# This is connection string for the database
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:12345678@localhost/fastapi"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# create engine is used to connect to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal class is a class that will be used to create a database session
# Why do we need a session?
# A session is a connection to the database that will be used to perform CRUD operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# declarative_base is a class that will be used to create models
# A model is a class that will be used to interact with the database
Base=declarative_base()

# Every model represents a table in our db

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


