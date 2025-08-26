from pydantic import BaseModel
from typing import List, Optional
from .diver import DiverOut

class GroupBase(BaseModel):
    name: str

class GroupCreate(GroupBase):
    """
    Schema for creating a new group. Only the name is required.
    The id is generated automatically by the database.
    """
    pass

class GroupOut(GroupBase):
    id: int
    divers: Optional[List[DiverOut]] = []

    model_config = {
        "from_attributes": True
    }
