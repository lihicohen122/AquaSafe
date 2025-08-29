from sqlalchemy.orm import Session
from database import SessionLocal

# FastAPI will call this function for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
