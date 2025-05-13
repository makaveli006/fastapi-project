
from fastapi import FastAPI, Body

app = FastAPI() # Create an instance of the FastAPI class
# Function + Decorator Block
# Decorator is a function that modifies another function
# Decorators are used to register functions as handlers for certain events
@app.get("/") # Decorator to define the path of the endpoint or path operation or route
# This path here references to the path that we go to in the browser
# This is a path operation decorator
# async is used to define a function as a coroutine it is optional but recommended
# async functions are used to define functions that can run asynchronously
# async functions can run concurrently with other functions
# async functions are non-blocking
async def root(): # Function that will be called when the endpoint is hit
    return {"message": "Hello World"} # it returns to user when the endpoint is hit # fast api converts to json thats how we see in browser or postman

# open cmd and run "uvicorn main:app" if port is not specified it will run on port 8000. "uvicorn main:app --reload" will reload the server when changes are made in the code
# This command runs it on port u like "uvicorn main:app --host 127.0.0.1 --port 8001" and "uvicorn main1_data_posting_without_restriction:app --host 127.0.0.1 --port 8001 --reload" will reload the server when changes are made in the code

# 127.0.0.1:8000 means our webserver is hosted in this specific URL.
# What is uvicorn?
# Uvicorn is a lightning-fast ASGI server implementation, using uvloop and httptools.
# ASGI is a standard interface between web servers and Python web application frameworks or toolkits.
# It stands for Asynchronous Server Gateway Interface.


@app.get("/posts")
def get_post():
    return {"message": "Hello Post"}

@app.post("/create_posts")
# Payload is a parameter is expected to be a dictionary (dict type annotation). It represents the JSON body sent by the client in the HTTP request.
def create_post(payload: dict = Body(...)): # Simply take the body from client request and convert to dictionary and store it in payload.
    # Body(...) is a dependency from FastAPI that extracts request body data. It is used to get the request body data from the client.
    # Body(...) is used to specify that payload should be extracted from the request body.
    # The ... (ellipsis) means that this parameter is required.
    # When using Body(...), it tells FastAPI to extract data from the request body.
    print(payload) # Prints the received JSON payload to the console/log for debugging. This helps developers verify the incoming data during API testing.
    return {"new_post": f"title {payload['title']} content: {payload['content']}"} # Returns a JSON response to the client. This is the response that the client will receive after the request is processed by the server.


# @app.post("/create_posts")
# def create_post(payload = Body(...)): 
#     print(type(payload)) # If we dont use a datatype assignment the Type is bytes here, so fast api does'nt know which data type we want to convert the incoming json data to
#     print(payload)
#     return {"message": "Post is created"}