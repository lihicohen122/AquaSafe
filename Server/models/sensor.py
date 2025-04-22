from pydantic import BaseModel

class Sensor(BaseModel):
    id: str
    bpm: int
    distance: int
    status: str  # "normal", "warning", "critical"