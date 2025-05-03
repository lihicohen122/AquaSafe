from sqlalchemy import Column, String, Integer, Float
from database import Base

class Diver(Base):
    __tablename__ = "divers"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    weight = Column(Float)
    contact_info = Column(String)
    bpm = Column(Integer)
    entry_point = Column(String)
    current_depth = Column(Float)
    status = Column(String)


# from pydantic import BaseModel

# class Diver(BaseModel):
#     id: str
#     name: str
#     age: int  # גיל
#     weight: float  # משקל בק"ג
#     contact_info: str  # פרטי קשר
#     bpm: int  # דופק
#     entry_point: str  # נקודת כניסה
#     current_depth: float  # עומק נוכחי במטרים
#     status: str  # "normal", "warning", "critical"