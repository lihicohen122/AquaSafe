from pydantic import BaseModel

class DiverBase(BaseModel):
    id: str
    name: str
    age: int
    weight: float
    contact_info: str
    bpm: int
    entry_point: str
    current_depth: float
    status: str

class DiverCreate(DiverBase):
    group_id: int | None = None

class DiverOut(DiverBase):
    group_id: int | None = None

    class Config:
        from_attributes = True  # New pydantic v2 attribute instead of orm_mode

class Diver(DiverBase):
    group_id: int | None = None

    class Config:
        from_attributes = True  # Updated to new pydantic v2 attribute