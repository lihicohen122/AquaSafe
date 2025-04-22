from pydantic import BaseModel

class Diver(BaseModel):
    id: str
    name: str
    age: int  # גיל
    weight: float  # משקל בק"ג
    contact_info: str  # פרטי קשר
    bpm: int  # דופק
    entry_point: str  # נקודת כניסה
    current_depth: float  # עומק נוכחי במטרים
    status: str  # "normal", "warning", "critical"