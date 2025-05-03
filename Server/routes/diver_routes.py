from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from managers.diver_manager import DiverManager
from schemas.diver import DiverCreate, DiverOut
from dependencies import get_db

router = APIRouter()

@router.get("/", response_model=List[DiverOut])
def get_divers(db: Session = Depends(get_db)):
    manager = DiverManager(db)
    return manager.get_all_divers()

@router.get("/{diver_id}", response_model=DiverOut)
def get_diver(diver_id: str, db: Session = Depends(get_db)):
    manager = DiverManager(db)
    diver = manager.get_diver_by_id(diver_id)
    if not diver:
        raise HTTPException(status_code=404, detail="Diver not found")
    return diver

@router.post("/", response_model=DiverOut)
def add_diver(diver: DiverCreate, db: Session = Depends(get_db)):
    manager = DiverManager(db)
    return manager.add_diver(diver)
