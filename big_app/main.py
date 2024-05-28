from fastapi import Depends, FastAPI

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users #this imports the routers from the routers folder

app = FastAPI(dependencies=[Depends(get_query_token)])

#including existing routers
app.include_router(users.router)
app.include_router(items.router)
#resetting the prefix for the admin router
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)
#also routers can be included in a router
#such as router.include_router(users.router)

#a simple root path operation
@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}