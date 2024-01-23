from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Union, Annotated

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

class User(BaseModel):
    username: str
    full_name: Annotated[str, "full name"]
    email: str
    disabled: bool = None
    
@app.put("/items/{item_id}")
#now put function will require a body that specifies the name of the base model
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    pass
