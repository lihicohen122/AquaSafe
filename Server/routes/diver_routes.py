from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
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
    try:
        # Check if diver with this ID already exists
        existing_diver = db.query(DiverModel).filter(DiverModel.id == diver.id).first()
        if existing_diver:
            raise HTTPException(
                status_code=409,
                detail=f"Diver with ID {diver.id} already exists"
            )
        
        new_diver = DiverModel(**diver.dict())
        db.add(new_diver)
        db.commit()
        db.refresh(new_diver)
        return new_diver
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail=f"Diver with ID {diver.id} already exists"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while creating the diver: {str(e)}"
        )

@router.delete("/{diver_id}")
def delete_diver(diver_id: str, db: Session = Depends(get_db)):
    diver = db.query(DiverModel).filter(DiverModel.id == diver_id).first()
    if not diver:
        raise HTTPException(status_code=404, detail="Diver not found")
    db.delete(diver)
    db.commit()
    return {"message": f"Diver {diver_id} deleted successfully"}
