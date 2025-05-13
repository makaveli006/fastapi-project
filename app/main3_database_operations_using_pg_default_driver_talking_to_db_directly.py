
from fastapi import FastAPI, Body,Response,status,HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()
# Pydantic models make sure that our front end is sending the correct data types and correct data
# Pydantic models also provide validation for the data that we are sending to the server
# Pydantic models also provide serialization and deserialization
# Pydantic models also provide documentation for the API
class Post(BaseModel): # Posts extends BaseModel
    title: str
    content: str
    published: bool = False # User doesnt need to provide this field, it will be False by default
    rating: Optional[int] = None # User doesnt need to provide this field, it will be None by default

while True:

    try:
        conn = psycopg2.connect(host="localhost",database="fastapi",user='postgres',password='12345678',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connected to the database!!")
        break
    except Exception as error:
        print("Error connecting to the database!!")
        print("Error was", error)
        time.sleep(2)
    

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts """) # It only define query, it does not execute it
    posts = cursor.fetchall() # It executes the query
    print(posts)
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED) # without status_code=status.HTTP_201_CREATED, it will return 200 status code
def create_post(post: Post):
    # cursor.execute(f"INSERT INTO posts (title, content, published) VALUES({new_post.title}, {new_post.content}, {new_post.published})") # Vulnerable to SQL injection
    # If post.title, post.content, or post.published contains malicious SQL code, it will be executed directly.
    # Example: If post.title = "title'); DROP TABLE posts; --", the query becomes:
    # INSERT INTO posts (title, content, published) VALUES('title'); DROP TABLE posts; --', 'some content', true)
    # This can delete the entire posts table!
    # SQL injection works by injecting malicious SQL syntax into user input.
    # The f-string method does not handle escaping for special characters properly.
#  =========================================================================================================
    # Instead of using f-strings, use parameterized queries like this the second line of the code:
    # Why is this safer?
    # The database engine treats values as data rather than SQL code.
    # It escapes special characters automatically, preventing SQL injection.
    # Conclusion:
    # Always use parameterized queries instead of string formatting (f-string, .format(), or + concatenation) to safely execute SQL statements.
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published)) # This avoids SQL injection
    # If no return * is used, the inserted row's data will not be returned.
    # This lets us confirm that a post was inserted successfully.
    # If None is returned, we know that the post was not inserted.
    new_post = cursor.fetchone() # After executing a SQL query using cursor.execute(), calling cursor.fetchone() will return: The first row of the result set as a tuple or a dictionary (depending on the database adapter used).
    conn.commit() # This commits the transaction like pressing the save button in the database or migrating the changes to the database
    return {"data": new_post}


# Getting a single post
@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} is not found")
    return {"post_detail": post}



@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    # In SQL, the RETURNING * clause is used in queries such as INSERT, UPDATE, or DELETE to return the affected rows immediately after executing the query. 
    cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    # The DELETE query removes the post with the given id.
    # The RETURNING * ensures that the deleted row's data is returned before it is deleted.
    # If no Returning * is used, the deleted row's data will not be returned.
    # This lets us confirm that a post existed before deleting it.
    # If None is returned, we know that the post did not exist.
    deleted_posts = cursor.fetchone()
    conn.commit()
    if deleted_posts == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} is not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")

def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # If no RETURNING * is used, the updated row's data will not be returned.
    # If we dont use where clause, all the rows will be updated
    updated_post = cursor.fetchone()
    conn.commit() # Anytime you make a change to the database, you need to commit it
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} is not found")
    return {"data": updated_post}
