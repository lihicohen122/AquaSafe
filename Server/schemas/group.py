from pydantic import BaseModel

class GroupBase(BaseModel):
    name: str

class GroupCreate(GroupBase):
    id: int

class GroupOut(GroupBase):
    id: int

    model_config = {
        "from_attributes": True
    }
