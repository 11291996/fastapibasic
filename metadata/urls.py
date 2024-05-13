from fastapi import FastAPI

#one can use openapi_url or absolute path for metadata
app = FastAPI(openapi_url="/api/v1/openapi.json")

@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]