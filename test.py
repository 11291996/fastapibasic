from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()

@app.post(
    "/items/",
    response_model=Item,
    summary="Create an item",
    response_description="The created item" #shown in the Reponse body in docs
)
async def create_item(item: Item):
    pass

#deprecated a path operation
@app.get("/elements/", tags=["items"], deprecated=True) #will be deprecated in the docs
async def read_elements(): #but still works
    return [{"item_id": "Foo"}]