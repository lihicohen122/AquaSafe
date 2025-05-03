from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from managers.group_manager import GroupManager
from schemas.group import GroupCreate, GroupOut
from dependencies import get_db

router = APIRouter()

@router.get("/", response_model=List[GroupOut])
def get_groups(db: Session = Depends(get_db)):
    manager = GroupManager(db)
    return manager.get_all_groups()

@router.post("/", response_model=GroupOut)
def add_group(group: GroupCreate, db: Session = Depends(get_db)):
    manager = GroupManager(db)
    return manager.add_group(group)