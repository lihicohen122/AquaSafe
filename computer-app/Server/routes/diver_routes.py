from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.diver import Diver as DiverModel
from schemas.diver import DiverCreate, DiverOut
from dependencies import get_db

router = APIRouter()

@router.get("/{diver_id}", response_model=DiverOut)
def get_diver(diver_id: str, db: Session = Depends(get_db)):
    diver = db.query(DiverModel).filter(DiverModel.id == diver_id).first()
    if not diver:
        raise HTTPException(status_code=404, detail="Diver not found")
    return diver

@router.post("/", response_model=DiverOut)
def create_diver(diver: DiverCreate, db: Session = Depends(get_db)):
    new_diver = DiverModel(**diver.dict())
    db.add(new_diver)
    db.commit()
    db.refresh(new_diver)
    return new_diver

@router.delete("/{diver_id}")
def delete_diver(diver_id: str, db: Session = Depends(get_db)):
    diver = db.query(DiverModel).filter(DiverModel.id == diver_id).first()
    if not diver:
        raise HTTPException(status_code=404, detail="Diver not found")
    db.delete(diver)
    db.commit()
    return {"message": f"Diver {diver_id} deleted successfully"}
