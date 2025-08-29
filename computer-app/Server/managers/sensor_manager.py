from typing import List
from models.sensor import Sensor
from managers.diver_manager import DiverManager

class SensorManager:
    def __init__(self, diver_manager: DiverManager):
        self.diver_manager = diver_manager

    def get_all_sensors(self):
        # Create a simplified list from the full data in DiverManager
        return [
            {
                "id": diver["id"],
                "name": diver["name"],
                "bpm": diver["bpm"],
                "current_depth": diver["current_depth"],  # Using current_depth
                "status": diver["status"],
            }
            for diver in self.diver_manager.divers
        ]