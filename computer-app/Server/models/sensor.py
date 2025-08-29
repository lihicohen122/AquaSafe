from pydantic import BaseModel

class Sensor(BaseModel):
    id: str
    bpm: int
    current_depth: float  # Current depth instead of distance
    status: str  # "normal", "warning", "critical"