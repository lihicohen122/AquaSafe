from sqlalchemy.orm import Session
from database import SessionLocal

# FastAPI יקרא לפונקציה הזו עבור כל בקשה
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
