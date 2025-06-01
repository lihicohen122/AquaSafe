from pydantic import BaseModel

class DiverBase(BaseModel):
    name: str
    age: int
    weight: float
    contact_info: str
    bpm: int
    entry_point: str
    current_depth: float
    status: str
    group_id: int  # שיוך לקבוצה

class DiverCreate(DiverBase):
    id: str  # מזהה ייחודי שמסופק מה-Frontend

class DiverOut(DiverBase):
    id: str

    model_config = {
    "from_attributes": True
    }
