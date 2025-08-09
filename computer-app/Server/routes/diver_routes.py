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

# This endpoint is used by the acoustic server - DO NOT MODIFY
@router.post("/", response_model=DiverOut)
def create_diver(diver: DiverCreate, db: Session = Depends(get_db)):
    new_diver = DiverModel(**diver.dict())
    db.add(new_diver)
    db.commit()
    db.refresh(new_diver)
    return new_diver

# New endpoint specifically for web form submissions
@router.post("/web", response_model=DiverOut)
def create_diver_web(diver: DiverCreate, db: Session = Depends(get_db)):
    # Check if diver with this ID already exists
    existing_diver = db.query(DiverModel).filter(DiverModel.id == diver.id).first()
    if existing_diver:
        raise HTTPException(status_code=400, detail=f"Diver with ID '{diver.id}' already exists")
    
    # Create new diver with group_id
    new_diver = DiverModel(
        id=diver.id,
        name=diver.name,
        age=diver.age,
        weight=diver.weight,
        contact_info=diver.contact_info,
        bpm=diver.bpm,
        entry_point=diver.entry_point,
        current_depth=diver.current_depth,
        status=diver.status,
        group_id=diver.group_id
    )
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
