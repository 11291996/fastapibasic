from fastapi import FastAPI, Path, Query
from typing import Annotated


app = FastAPI()

@app.get("/items/{item_id:path}")
#this will give an error if q is not defined with fastapi
async def read_items(item_id: str = Path(), q: str = Query()):
    pass

if __name__ == "__main__":
    pass