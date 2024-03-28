#sql databases
#fastapi does not need sql databases but it is compatible with them
#recall object relational mapping from djangobasic
#install SQLAlchemy with command "pip install sqlalchemy" to enable object relational mapping

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#set the database url
#one has to make this url with the prior knowledge of the database 
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

#creating the engine that will start the mapping
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
#check_same_thread is set given for SQLite, but not for other databases
#this is because SQLite tries to use the same thread always
#but this argument will allow the engine to use different threads

#this instance will actually execute object relational mapping
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#this will store the models
Base = declarative_base()