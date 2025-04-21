from pydantic import BaseModel
from typing import List

# Define a model for a group
class Group(BaseModel):
    id: int
    name: str

# GroupManager class to handle group-related logic
class GroupManager:
    def __init__(self):
        self.groups = [
            {"id": 1, "name": "Coral Divers"},
            {"id": 2, "name": "Deep Sea Explorers"},
            {"id": 3, "name": "Blue Ocean Team"},
        ]

    def get_all_groups(self) -> List[Group]:
        return self.groups

    def add_group(self, group: Group) -> Group:
        self.groups.append(group.model_dump())
        return group