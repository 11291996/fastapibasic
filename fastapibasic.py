#very pythonic program
#strongly based on pydantic and typing module

from fastapi import FastAPI

app = FastAPI()

@app.get("/") #this address 
async def root(): #is handled by this function #async handles the function asynchronously
    return {"message": "Hello World"}

#run uvicorn fastapibasic:app --reload in terminal
#--reload: make the server restart after code changes. Only use for development.
#http://127.0.0.1:8000/docs -> swagger ui for api documentation
#http://127.0.0.1:8000/redoc -> redoc ui

#http methods: get, post, put, delete, options, head, patch, trace can be used as decorators
@app.post("/1")
def post():
    pass

@app.put("/2")
def put():
    pass

@app.delete("/3")
def delete():
    pass

@app.options("/4")
def options():
    pass

@app.head("/5")
def head():
    pass

@app.patch("/6")
def patch():
    pass

@app.trace("/7")
def trace():
    pass

#usage of api like django's views urls.py file

@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id} 

@app.get("/nums/{num}")
async def read_num(num: int): #data type can be specified #conversion will be automatic
    return {"nums": num}

#if data type cannot be converted, it will return an error with OpenAPI schema

#mind the orders 

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

#in this case if the second function is placed before the first one, the first will call me not the current user

#redefining is impossible

@app.get("/users")
async def read_users():
    return ["Rick", "Morty"]


@app.get("/users")
async def read_users2():
    return ["Bean", "Elfo"]

#in this case the api will always return ["Rick", "Morty"]

#using optional parameters with Enum
from enum import Enum

class ModelName(str, Enum): #type detection is possible
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName): #type detection is also possible
    if model_name is ModelName.alexnet: #with FastAPI you can use Enum instance's attribute and its name interchangeably  
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.name == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"} #automatic deals with the left over case

#options are well documented in the swagger ui when enum is used

#path parameter 
@app.get("/files/{file_path:path}") #this enables the path to contain slashes
async def read_file(file_path: str): 
    return {"file_path": file_path}
