from fastapi import APIRouter
from typing import List
from managers.group_manager import GroupManager
from models.group import Group

router = APIRouter()
group_manager = GroupManager()

@router.get("/", response_model=List[Group])
def get_groups():
    return group_manager.get_all_groups()

@router.post("/", response_model=Group)
def add_group(group: Group):
    return group_manager.add_group(group)