from typing import List
from models.diver import Diver

class DiverManager:
    def __init__(self):
        self.divers = [
            {"id": 1, "name": "Lihi", "bpm": 80, "distance": 12, "status": "normal"},
            {"id": 2, "name": "Noa", "bpm": 77, "distance": 14, "status": "normal"},
        ]

    def get_all_divers(self) -> List[Diver]:
        return self.divers

    def add_diver(self, diver: Diver) -> Diver:
        self.divers.append(diver.dict())
        return diver