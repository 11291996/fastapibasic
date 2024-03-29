from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
                
import crud, models, schemas
from database import SessionLocal, engine

#import already imported Base from models
#connect it with the engine from database
#one can also use Alembic to start the database and migrations like in djangobasic  
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#use the crud functions to create a new user
@app.post("/users/", response_model=schemas.User)
#for SQLAlchemy, asynchronous functions cannot be used since most SQL's are synchronous
#to use asynchronous databases and connect them with FastAPI, use other databases and ORMs
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

#use the crud functions to get all users
@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

#use the crud functions to get a user by id
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

#use the crud functions to create an item for a user
@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)

#use the crud functions to get all items
@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)