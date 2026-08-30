from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#Database connection string
DATABASE_URL = "postgresql://mac@localhost:5432/study_planner"

#Engine
engine = create_engine(DATABASE_URL)

#Session we will make queries to the database
SessionLocal = sessionmaker(autocommit = False, autoflash = False, bind = engine)

#Base - all our tables will inherit from it
Base = declarative_base()

def get_db():
    """This function creates a "session" (connection) for a single 
    request and always closes it afterward, even if there was an 
    error. We'll use it in main.py via Depends(get_db)."""
    bd = SessionLocal
    try:
        yield db
    finally: 
        db.close()