from sqlalchemy.orm import Session
from models.group import Group as GroupModel
from schemas.group import GroupCreate
from sqlalchemy.orm import joinedload
from fastapi import HTTPException

class GroupManager:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_all_groups(self):
        return self.db.query(GroupModel).options(joinedload(GroupModel.divers)).all()

    def add_group(self, group: GroupCreate):
        # Check if group name already exists
        existing_group = self.db.query(GroupModel).filter(GroupModel.name == group.name).first()
        if existing_group:
            raise HTTPException(status_code=400, detail="Group name already exists")
            
        db_group = GroupModel(**group.dict())
        self.db.add(db_group)
        self.db.commit()
        self.db.refresh(db_group)
        return db_group
