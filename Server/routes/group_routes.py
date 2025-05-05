from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from managers.group_manager import GroupManager
from schemas.group import GroupCreate, GroupOut
from models.group import Group as GroupModel
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

@router.get("/{group_id}", response_model=GroupOut)
def get_group_by_id(group_id: int, db: Session = Depends(get_db)):
    group = db.query(GroupModel).options(joinedload(GroupModel.divers)).filter(GroupModel.id == group_id).first()
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return group
