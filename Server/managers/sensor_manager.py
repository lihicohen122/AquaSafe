from typing import List
from models.sensor import Sensor

class SensorManager:
    def __init__(self):
        self.sensors = [
            {"id": "Lihi", "bpm": 80, "distance": 12, "status": "normal"},
            {"id": "Noa", "bpm": 77, "distance": 14, "status": "normal"},
            {"id": "Adva", "bpm": 160, "distance": 25, "status": "critical"},
            {"id": "Adi", "bpm": 110, "distance": 20, "status": "warning"},
        ]

    def get_all_sensors(self) -> List[Sensor]:
        return self.sensors