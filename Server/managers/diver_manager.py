from sqlalchemy.orm import Session
from models.diver import Diver as DiverModel
from schemas.diver import DiverCreate

class DiverManager:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_all_divers(self):
        return self.db.query(DiverModel).all()

    def get_diver_by_id(self, diver_id: str):
        return self.db.query(DiverModel).filter(DiverModel.id == diver_id).first()

    def add_diver(self, diver: DiverCreate):
        db_diver = DiverModel(**diver.dict())
        self.db.add(db_diver)
        self.db.commit()
        self.db.refresh(db_diver)
        return db_diver
