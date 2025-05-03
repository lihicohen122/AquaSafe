from sqlalchemy.orm import Session
from models.group import Group as GroupModel
from schemas.group import GroupCreate
from sqlalchemy.orm import joinedload

class GroupManager:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_all_groups(self):
        return self.db.query(GroupModel).options(joinedload(GroupModel.divers)).all()

    def add_group(self, group: GroupCreate):
        db_group = GroupModel(**group.dict())
        self.db.add(db_group)
        self.db.commit()
        self.db.refresh(db_group)
        return db_group
