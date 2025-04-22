from fastapi import APIRouter, HTTPException
from typing import List
from managers.diver_manager import DiverManager
from models.diver import Diver

router = APIRouter()
diver_manager = DiverManager()

@router.get("/", response_model=List[Diver])
def get_divers():
    return diver_manager.get_all_divers()

@router.get("/{diver_id}", response_model=Diver)
def get_diver(diver_id: str): 
    diver = diver_manager.get_diver_by_id(diver_id)
    if not diver:
        raise HTTPException(status_code=404, detail="Diver not found")
    return diver

@router.post("/", response_model=Diver)
def add_diver(diver: Diver):
    return diver_manager.add_diver(diver)