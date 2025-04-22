from pydantic import BaseModel

class Sensor(BaseModel):
    id: str
    bpm: int
    current_depth: float  # עומק נוכחי במקום distance
    status: str  # "normal", "warning", "critical"