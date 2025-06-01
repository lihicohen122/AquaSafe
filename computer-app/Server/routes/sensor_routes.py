from fastapi import APIRouter
from typing import List
from managers.sensor_manager import SensorManager
from models.sensor import Sensor

router = APIRouter()
sensor_manager = SensorManager()

@router.get("/", response_model=List[Sensor])
def get_sensors():
    return sensor_manager.get_all_sensors()