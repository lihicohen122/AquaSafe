from pydantic import BaseModel

class Diver(BaseModel):
    id: int
    name: str
    bpm: int  # Heart rate
    distance: int  # Distance in meters
    status: str  # "normal", "warning", "critical"