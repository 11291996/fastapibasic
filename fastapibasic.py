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

