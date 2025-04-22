from pydantic import BaseModel
from typing import List
from models.diver import Diver

class Group(BaseModel):
    id: int
    name: str
    divers: List[Diver] = []