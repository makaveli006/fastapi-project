
from fastapi import FastAPI, Body,Response,status,HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange

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

my_posts = [
    {
        "title": "title of post 1",
        "content": "content of post 1",
        "id": 1
    },
    {
        "title": "favorite foods",
        "content": "I like pizza",
        "id": 2
    }
]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED) # without status_code=status.HTTP_201_CREATED, it will return 200 status code
def create_post(new_post: Post):
    post_dict = new_post.dict()
    post_dict["id"] = randrange(0,100000)
    my_posts.append(post_dict)
    return {"data":post_dict}



@app.get("/posts/{id}")  # {id} is a path parameter
# fast api will automatically convert the id to an integer
def get_post(id: int, response: Response): # With just "def get_post(id):" when we send a request it raises internal server error, but when we specify the type of id as int, it responds saying "Input should be a valid integer, unable to parse string as an integer"
    # And we no longer need to convert the id to int, fast api will do it for us when we specify the type of id as int
    # post = find_post(int(id))
    post = find_post(id)
    if not post: # if http://localhost:8001/posts/17 is entered, it will return "Post not found" because there is no post with id 17
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} is not found") # This cleaner than below two lines of code, this does the same with the below 2 line.
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"data": f"Post with {id} is not found"}
    return {"post_detail": post}

# @app.post("/create_posts")
# def create_post(new_post: Post):
#     print(new_post)
#     print(type(new_post))
#     # If we want to convert a pydantic model to a dictionary, we can use the dict() function
#     print(dict(new_post))
#     return {"data":new_post}
#     # return {"data": f"title is {new_post.title} and content is {new_post.content} and published is {new_post.published} and rating is {new_post.rating}"}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    # deleting post
    # find the index in the array that has required id
    # my_posts.pop(index)
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} is not found")
    my_posts.pop(index)
    # return {'message': 'post was successfully deleted'} # we dont want to return data to client if
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
# Client sends the data in the body of the request through front end and we receive it in the post parameter
# Then we find the index of the post with the id that the client wants to update
# Then we convert the pydantic model to a dictionary
# Then we add the id to the dictionary
# Then we update the post in the my_posts array with the new post
# Then we return the updated post
# Then we return a message to the client

def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} is not found")
    post_dict = post.dict()
    # print(post_dict)
    post_dict["id"] = id
    # print(post_dict)
    my_posts[index] = post_dict
    return {"data": post_dict}
    # return {"message": "post has been updated"}