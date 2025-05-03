from pydantic import BaseModel
from typing import List
from schemas.diver import DiverOut as Diver

class Group(BaseModel):
    id: int
    name: str
    divers: List[Diver] = []