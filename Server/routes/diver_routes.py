from fastapi import APIRouter
from typing import List
from managers.diver_manager import DiverManager
from models.diver import Diver

router = APIRouter()
diver_manager = DiverManager()

@router.get("/", response_model=List[Diver])
def get_divers():
    return diver_manager.get_all_divers()

@router.post("/", response_model=Diver)
def add_diver(diver: Diver):
    return diver_manager.add_diver(diver)