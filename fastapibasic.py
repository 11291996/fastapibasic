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

#query parameter -> non path parameters
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

#http://127.0.0.1:8000/items/?skip=0&limit=10 -> use this convention to pass multiple parameters
#if one of them is or both are not defined, it will use the default value

#using python annotations
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

#type conversion 
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

#multiple path and query parameters
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

#if default value is not defined, it will be required
@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy} #if needy is not defined, it will return an error
    return item

#request body
#one can send json, form data, files, etc. to the server through request body
#to declare a request body, use pydantic models
#the browser will normally send the data to the api 
#but one can test the api with swagger ui or curl
from pydantic import BaseModel

#similar logic with query parameters with default values
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/")
async def create_item(item: Item):
    return item

#application of request body
#editor support is possible like mentioned above
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

#request body + path parameter

@app.put("/items/{item_id}") #put is used for updating
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item}

#request body + path parameter + query parameter

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item_id}
    if q:
        result.update({"q": q})
    return result

#query parameter and string validation
from typing import Annotated
from fastapi import Query

@app.get("/items/")
#use Query and Annotated to validate query parameter
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None): 
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.get("/items/")
async def read_items(
    q: Annotated[str | None, Query(min_length=3, max_length=50)] = None #min_length is also possible
):
    pass

@app.get("/items/")
#adding regular expression as a validation
async def read_items(
    q: Annotated[
        str | None, Query(min_length=3, max_length=50, pattern="^fixedquery$")
    ] = None,
):
    pass 

#default values with validation
@app.get("/items/")
async def read_items(q: Annotated[str, Query(min_length=3)]):
    pass

#using ellipsis to make a parameter required

@app.get("/items/")
async def read_items(q: Annotated[str, Query(..., min_length=3)]):
    pass

#None is allowed but still required

@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(min_length=3)] = ...):
    pass

#multiple values and query parameter list
#checking with docs is recommended
@app.get("/items/")
async def read_items(q: Annotated[list[str] | None, Query()] = None):
    pass

#with default values
@app.get("/items/")
async def read_items(q: Annotated[list[str], Query()] = ["foo", "bar"]):
    pass

#type free list 

@app.get("/items/")
async def read_items(q: Annotated[list, Query()]):
    pass

#meta data can be added like this
@app.get("/items/")
async def read_items(
    q: Annotated[str | None, Query(title="Query string", min_length=3)] = None
):
    pass
#also description is possible
@app.get("/items/")
async def read_items(
    q: Annotated[
        str | None,
        Query(
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
        ),
    ] = None,
):
    pass

#alias query parameter
@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(alias="item-query")] = None):
    pass

#this will make the query not be in the schema and so not be documented in docs
@app.get("/items/")
async def read_items(
    hidden_query: Annotated[str | None, Query(include_in_schema=False)] = None
):
    pass

#path parameter and number validation

from fastapi import Path #use Path to validate path parameter

#Path checks item_id's type is path
@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")], #adding meta data
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

#order of parameters in python function is important
#if a parameter with a default value is placed before a parameter without a default value, it will give an error
#but for fastapi, it is not important
@app.get("/items/{item_id}")
async def read_items(q: str, item_id: int = Path(title="The ID of the item to get")):
    pass

