from typing import List
from models.group import Group

class GroupManager:
    def __init__(self):
        self.groups = [
            {"id": 1, "name": "Coral Divers", "divers": []},
            {"id": 2, "name": "Deep Sea Explorers", "divers": []},
        ]

    def get_all_groups(self) -> List[Group]:
        return self.groups

    def add_group(self, group: Group) -> Group:
        self.groups.append(group.dict())
        return group