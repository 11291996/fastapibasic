#very pythonic program
#strongly based on python annotation, pydantic and typing module

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

#default values
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10): #theses are query parameters
    return fake_items_db[skip : skip + limit]

#http://127.0.0.1:8000/items/?skip=0&limit=10 -> use this convention to pass multiple parameters
#if one of them is or both are not defined, it will use the default value
#if None is set as default value, it will be not required

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
    return {"item_id": item_id, "item": item.name}

#request body + path parameter + query parameter

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, "item": item.name}
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
#this will give an error if q is not defined with fastapi
async def read_items(item_id: int = Path(), q: str = Query()):
    pass
#simply using Annotated will solve this problem
@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")], q: str
):
    pass
#trick 
@app.get("/items/{item_id}")
#the star will call the arguments in the function as keyword arguments, so the order is not important
async def read_items(*, item_id: int = Path(title="The ID of the item to get"), q: str):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

#numeric validation
@app.get("/items/{item_id}")
#greater or equal to 1
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=1)], q: str
):
    pass
#greater than 0 or less than 100
@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get", gt=0, lt=100)],
    q: str,
):
    pass
#using float
@app.get("/items/{item_id}")
async def read_items(
    *,
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str,
    size: Annotated[float, Query(gt=0, lt=10.5)],
):
    pass

#multiple path, query and body parameters
from typing import Union

@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: Union[str, None] = None,
    item: Union[Item, None] = None,
):
    pass

#multiple body parameters

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

class User(BaseModel):
    username: str
    full_name: Union[str, None] = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results

#singular value body
from fastapi import Body

@app.put("/items/{item_id}")
async def update_item(
    item_id: int, item: Item, user: User, importance: Annotated[int, Body()]):
    pass

#embedding the only body parameter
@app.put("/items/{item_id}")
#now put function will require a body that specifies the name of the base model
#embedding is automatically done when there are multiple body parameters
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    pass

#using pydantic to add validation and metedata 
from pydantic import Field

class Item(BaseModel):
    name: str
    #adding metadata and validation
    description: Union[str, None] = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: Union[float, None] = None

#generic keys for pydantic models
class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: list = [] #this can be replaced with pydantic's List[str] for better type checking
    #other generic types are possible 

#nested models
#keys can be other models
class Image(BaseModel):
    url: str
    name: str
#nested model
class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: set[str] = set()
    image: Union[Image, None] = None #a model key

#http type check and more 
from pydantic import HttpUrl

class Image(BaseModel):
    url: HttpUrl #this will check if the input is http url 
    name: str #also many other types are possible. check pydantic docs

#generic submodel 
    
class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: set[str] = set()
    images: Union[list[Image], None] = None #a submodel list 

#deeply nested models

class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: set[str] = set()
    images: Union[list[Image], None] = None

class Offer(BaseModel): #model in model in model
    name: str
    description: Union[str, None] = None
    price: float
    items: list[Item]

@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer

#getting input as a list 
@app.post("/images/multiple/")
async def create_multiple_images(images: list[Image]): #editor support is possible
    return images
#getting input as a dict
@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    return weights

#adding examples to via pydantic model

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    model_config = { #this will be shown as an example in the docs
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        }
    }

#using Field to add examples
class Item(BaseModel):
    name: str = Field(examples=["Foo"])
    description: Union[str, None] = Field(default=None, examples=["A very nice Item"])
    price: float = Field(examples=[35.4])
    tax: Union[float, None] = Field(default=None, examples=[3.2])

#adding examples via fastapi

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Annotated[
        Item,
        Body(
            examples=[
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ],
        ),
    ],
):
    pass

#adding multiple examples via fastapi
@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Annotated[
        Item,
        Body(
            examples=[
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
                {
                    "name": "Bar",
                    "price": "35.4",
                },
                {
                    "name": "Baz",
                    "price": "thirty five point four",
                },
            ],
        ),
    ],
):
    pass

#cookie from djangobasic
from fastapi import Cookie

@app.get("/items/")
async def read_items(ads_id: Annotated[Union[str, None], Cookie()] = None): #cookie parameter declaration
    return {"ads_id": ads_id}

#header parameter from djangobasic
from fastapi import Header

@app.get("/items/")
async def read_items(user_agent: Annotated[Union[str, None], Header()] = None):
    return {"User-Agent": user_agent}
#http headers use hyphens, but python does not allow hyphens in variable names
#so autoconversion is done by fastapi
@app.get("/items/")
async def read_items(
    strange_header: Annotated[
        Union[str, None], Header(convert_underscores=False) #this will disable autoconversion
    ] = None,
):
    return {"strange_header": strange_header}
#multiple values for a header
@app.get("/items/")
async def read_items(x_token: Annotated[Union[list[str], None], Header()] = None):
    return {"X-Token values": x_token}

#responsing 
#use python annotation like above
@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item

@app.get("/items/")
async def read_items() -> list[Item]: #this will validate the response
    #also schema will be generated for docs
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
    ]

#if one wants to use basic python types for ease of use in the function
#but return pydantic models for documentation and validation
#use response_model
from typing import Any

#the function is using python type
#but will return the pydantic model which supports validation and documentation
@app.get("/items/", response_model=list[Item])
async def read_items() -> Any:
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]

#using response_model for security
from pydantic import EmailStr

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None

#this may send the user's password when the model is used for other paths
@app.post("/user/")
async def create_user(user: UserIn) -> UserIn:
    return user

class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

#so use response_model to prevent this
@app.post("/user/", response_model=UserOut) #autoconversion is done by pydantic
async def create_user(user: UserIn) -> Any:
    return user

#using inheritance to solve the problem above
class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class UserIn(BaseUser):
    password: str


@app.post("/user/")
async def create_user(user: UserIn) -> BaseUser:
    return user #this will also enable editor support ulike response_model above

#other return types
from fastapi import Response
#these are subclasses of Response, so the method above is being used
from fastapi.responses import JSONResponse, RedirectResponse

@app.get("/portal")
async def get_portal(teleport: bool = False) -> Response:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return JSONResponse(content={"message": "Here's your interdimensional portal."})

#response class cannot be used with nonresponse class unless something is done
#this will give an error
@app.get("/portal")
async def get_portal(teleport: bool = False) -> Response | dict:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return {"message": "Here's your interdimensional portal."}
#response model should be set to None then there is no error
@app.get("/portal", response_model=None)
async def get_portal(teleport: bool = False) -> Response | dict:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return {"message": "Here's your interdimensional portal."}
#assume that a function has a default response model, but one wants to return a response independent from the default
#but allow pydantic to validate the response and document it automatically
#use this argument

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True) #this will exclude the default values
#if the argument is set to False, the default values will be included by pydantic
async def read_item(item_id: str):
    return items[item_id]

#selecting certain keys from the model 
@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "description"}, #the model will only include these keys
)
async def read_item_name(item_id: str):
    return items[item_id]

@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"}) #this will exclude the tax key
async def read_item_public_data(item_id: str):
    return items[item_id]
#use pydantic dict to utilize multiple models
#multiple response models
class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type: str = "car"


class PlaneItem(BaseItem):
    type: str = "plane"
    size: int


items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}

@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    return items[item_id]

#getting as a dict is also possible
from typing import Dict

@app.get("/keyword-weights/", response_model=Dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}

#status code 
#http status code in network study 
@app.post("/items/", status_code=201)
async def create_item(name: str):
    return {"name": name}

#checking status code 
from fastapi import status

@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}

#form data
#non json schema data, decoded in html form
#so, different from query parameters
from fastapi import Form
@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}

#file data 
from fastapi import File, UploadFile
#File turns the file into bytes and uploads it to memory
@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}
#this will upload the file to the memory also but if it is too large, it will be saved to disks
#also metadata is available 
#see pythonbasic's file open part and refer docs for more info
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
#optional
@app.post("/files/")
async def create_file(file: Annotated[Union[bytes, None], File()] = None):
    pass
#adding metadata
@app.post("/files/")
async def create_file(file: Annotated[bytes, File(description="A file read as bytes")]):
    pass
#multiple files
#uses list
@app.post("/files/")
async def create_files(files: Annotated[list[bytes], File()]):
    return {"file_sizes": [len(file) for file in files]}

#handling errors
from fastapi import HTTPException
items = {"foo": "The Foo Wrestlers"}

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items: #with python if statement
        raise HTTPException(status_code=404, detail="Item not found") #automatically http error handled by fastapi
    return {"item": items[item_id]} #although this kind will be handled by fastapi without the if statement

#custom error handling
from fastapi import Request

class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(UnicornException) #this api will handle the custom exception defined above
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )

@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}

#overriding the default exception handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

@app.exception_handler(StarletteHTTPException) #fastapi's http exception inherits from starlette's
async def http_exception_handler(request, exc): #fastapi accepts json response and starlette accepts plain text response
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code) #but for exception handler, it is safer to change starlette's

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.") #no json response
    return {"item_id": item_id}

#using json format for error handling
#this can be used for normal functions
from fastapi.encoders import jsonable_encoder

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

class Item(BaseModel):
    title: str
    size: int

@app.post("/items/")
async def create_item(item: Item): #internal call for errors will use the request validation defined above 
    return item

#using default and custom exception handlers together
from fastapi.exception_handlers import (
    http_exception_handler, #this will be used as default exception handler
    request_validation_exception_handler,
)

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}

#tags
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()

#function discription will be shown in the docs
#dash will be replaced with space and the first letter will be capitalized
#also api will be grouped by tags
@app.post("/items/", response_model=Item, tags=["items"])
async def create_item(item: Item):
    return item

@app.get("/items/", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]

@app.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]

#tagging with oop 
class Tags(Enum):
    items = "items"
    users = "users"

@app.get("/items/", tags=[Tags.items])
async def get_items():
    return ["Portal gun", "Plumbus"]

@app.get("/users/", tags=[Tags.users])
async def read_users():
    return ["Rick", "Morty"]

#adding summary and description
#this will be shown in the docs
@app.post(
    "/items/",
    response_model=Item,
    summary="Create an item",
    description="Create an item with all the information, name, description, price, tax and a set of unique tags",
)
async def create_item(item: Item):
    return item

#use markdown with docstring
#this will be shown in the docs
@app.post("/items/", response_model=Item, summary="Create an item")
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item

#response description
@app.post(
    "/items/",
    response_model=Item,
    summary="Create an item",
    response_description="The created item" #
)
async def create_item(item: Item):
    pass

#deprecated a path operation
@app.get("/elements/", tags=["items"], deprecated=True) #will be deprecated in the docs
async def read_elements(): #but still works
    return [{"item_id": "Foo"}]

#partial update
#patch is used for partial update
@app.patch("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.model_dump(exclude_unset=True) #this will exclude the default values
    updated_item = stored_item_model.model_copy(update=update_data) #this will copy the model partially
    items[item_id] = jsonable_encoder(updated_item) #this will update the item partially
    return updated_item

#dependency injection
from fastapi import Depends

#one can use non async function as a dependency
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
#now the dependency function will get the parameters first 
#then the path operation function will receive the parameters
#by this, dependency injection is done
#also this method can be used for OpenAPI schema
#and like that, with right dependency, other programs like databases and packages will be compatible
#dependency can take the role of integrations and plugins as well
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons

#sharing dependency
CommonsDep = Annotated[dict, Depends(common_parameters)]

@app.get("/users/")
async def read_users(commons: CommonsDep):
    return commons

#security
from fastapi.security import OAuth2PasswordBearer
#fastapi's module based on a thrid party security library called OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#since OAuth2 module is involved, the docs will show authorization button including username and password
#normally, OAuth2 will send the information to independent server but fastapi sends it to the tokenUrl above
#the python code will be like this "response = requests.get(URL, headers={"Authorization":"Bearer token"})"
#similar to https' request header
#then the url will send back a token as the reponse that authenticates the user and expires after a certain time
#this way will be safer for other user interferences
#does the same role as django's escape function
#frontend will store the token and utilize it for requests that need authentications
@app.get("/items/")
#this dependency will check that the input of the function is from OAuth2 module
#this will return authentication error already if the input is not from OAuth2
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
#returning user info from the token
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user

@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

#creating a login system
from fastapi.security import OAuth2PasswordRequestForm
#user database 
#in docs, enter the username and password with hashing then it will login
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}
#fake hashing
def fake_hash_password(password: str):
    return "fakehashed" + password

class UserInDB(User):
    hashed_password: str

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token")
#OAuth2PasswordRequestForm will be used for the form data including username and password
#scope also will be included and used to identify the user's access level
#user:read, user:write, admin:read, admin:write, etc. are the examples of scope
#this code enables the login system as OAuth2PasswordBearer is set to this path(/token)
#If the depedency(OAuth2PasswordRequestForm) passes the function below without error, FastAPI will successfully authenticate the user
#So there are lines that raises errors if the user is not found or the password is incorrect
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}

#security level hashing
#uses Json Web Tokens(JWT) to ready the token for encryption
#install python-jose and passlib

from jose import JWTError, jwt
from passlib.context import CryptContext
#for token expiration time
from datetime import datetime, timedelta, timezone

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
#algorithm for encryption
ALGORITHM = "HS256"
#token expire time variable
ACCESS_TOKEN_EXPIRE_MINUTES = 30
#if these are hacked, it can be very dangerous

oauth2_scheme_real = OAuth2PasswordBearer(tokenUrl="real_token")

#class to store the token data
class Token(BaseModel):
    access_token: str
    token_type: str
#class to store token corresponding data
class TokenData(BaseModel):
    username: str | None = None

#passlib instance for encryption
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db_real = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        #this is jwt and passlib encrypted password of "secret"
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

#checking the hashed password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

#hashing the password
def get_password_hash(password):
    return pwd_context.hash(password)

#comparing from the database
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

#creates a token with expiration time
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    #adding expiration time to the token
    to_encode.update({"exp": expire})
    #using jwt to encrypt the token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#checking the user from the database
async def get_current_user_real(token: Annotated[str, Depends(oauth2_scheme_real)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        #using jwt to decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        #storing the token corresponding data
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    #checking and returning the user from the database
    user = get_user(fake_users_db_real, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

#for raising current user error
async def get_current_active_user_real(
    current_user: Annotated[User, Depends(get_current_user_real)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

#real working login path
@app.post("/real_token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = authenticate_user(fake_users_db_real, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    #creates expiration time for the token using set variable
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    #creates the token
    access_token = create_access_token(
        #jwt notation for the subject of the token
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

#uses jwt and passlib to get the current user
@app.get("/users/current_me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user_real)]
):
    return current_user

#uses jwt and passlib to get the current user's items
@app.get("/users/current_me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user_real)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]

#similarly one can store the user data in the database and use it for the login

#middleware -> functions that run before every request and response

import time 

#this middleware adds the process time to the response header
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

#cross origin resource sharing -> when the backend is in different domain from the frontend
#port difference also applies
#when one tries to cross origin, the browser will send options request to the backend
#then the backend will respond with a header that allows the frontend to access the right backend
#To do this, the backend must have a list of allowed origins

#wildcards "*" -> allows all origins, just like djangobasic

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def main():
    return {"message": "Hello World"}

