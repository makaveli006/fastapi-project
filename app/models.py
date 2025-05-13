from sqlalchemy import Column, Integer, String,Boolean, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
# Base class is used to create models

# The bwlow code is used to create a Post model
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    # server_default='TRUE' means that the default value of the field will be TRUE in the database
    published = Column(Boolean,server_default='TRUE',nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    owner_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False) 
    owner = relationship("User") # This is used to create a relationship between the Post and User models
    # Meaning of above line:
    # owner_id is a foreign key that references the id column of the users table
    # ondelete="CASCADE" means that if the user is deleted, all the posts of the user will be deleted as well



# The below code is used to create a User model
# Does the below class directly creates table in db?
# No, the below class does not directly create table in db
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True,autoincrement=True,nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)
    # ondelete="CASCADE" means that if the user is deleted, all the votes of the user will be deleted as well
    # ondelete="CASCADE" means that if the post is deleted, all the votes of the post will be deleted as well