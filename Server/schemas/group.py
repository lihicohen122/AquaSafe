from pydantic import BaseModel
from typing import List, Optional
from .diver import DiverOut

class GroupBase(BaseModel):
    name: str

class GroupCreate(GroupBase):
    pass

class GroupOut(GroupBase):
    id: int
    divers: Optional[List[DiverOut]] = []

    model_config = {
        "from_attributes": True
    }
