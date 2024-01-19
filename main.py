from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

#similar logic with query parameters with default values
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/")
async def create_item(item: Item):
    return item