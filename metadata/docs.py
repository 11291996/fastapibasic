from fastapi import FastAPI

#now docs path is /documentation
#if one deletes the docs_url and add redoc_url, redoc ui will be shown with related url
app = FastAPI(docs_url="/documentation", redoc_url=None)

@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]