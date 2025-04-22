from typing import List
from models.diver import Diver

class DiverManager:
    def __init__(self):
        self.divers = [
            {
                "id": "Lihi",
                "name": "Lihi",
                "age": 28,
                "weight": 65.5,
                "contact_info": "lihi@example.com",
                "bpm": 80,
                "entry_point": "North Beach",
                "current_depth": 12.5,
                "status": "normal",
            },
            {
                "id": "Noa",
                "name": "Noa",
                "age": 32,
                "weight": 60.0,
                "contact_info": "noa@example.com",
                "bpm": 77,
                "entry_point": "South Dock",
                "current_depth": 14.0,
                "status": "normal",
            },
            {
                "id": "Adi",
                "name": "Adi",
                "age": 25,
                "weight": 58.0,
                "contact_info": "adi@example.com",
                "bpm": 110,
                "entry_point": "East Bay",
                "current_depth": 20.0,
                "status": "critical",
            },
            {
                "id": "Adva",
                "name": "Adva",
                "age": 30,
                "weight": 62.0,
                "contact_info": "adva@example.com",
                "bpm": 95,
                "entry_point": "West Cove",
                "current_depth": 18.0,
                "status": "warning",
            },
        ]

    def get_all_divers(self) -> List[Diver]:
        return self.divers

    def get_diver_by_id(self, diver_id: str) -> Diver:
        diver = next((d for d in self.divers if d["id"].lower() == diver_id.lower()), None)
        if diver:
            return Diver(**diver)
        return None
