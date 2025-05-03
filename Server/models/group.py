from sqlalchemy import Column, Integer, String
from database import Base

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)


# from pydantic import BaseModel
# from typing import List
# from schemas.diver import DiverOut as Diver

# class Group(BaseModel):
#     id: int
#     name: str
#     divers: List[Diver] = []