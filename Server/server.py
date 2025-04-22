from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from models.group import Group
from models.sensor import Sensor
from managers.group_manager import GroupManager
from managers.sensor_manager import SensorManager


app = FastAPI()

# Allow CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create instances of managers
group_manager = GroupManager()
sensor_manager = SensorManager()

# Routes for groups
@app.get("/groups", response_model=List[Group])
def get_groups():
    return group_manager.get_all_groups()

@app.post("/groups", response_model=Group)
def add_group(group: Group):
    return group_manager.add_group(group)

# Routes for sensors
@app.get("/sensors", response_model=List[Sensor])
def get_sensors():
    return sensor_manager.get_all_sensors()

@app.get("/")
def read_root():
    return {"message": "Hello from Diver Distress System!"}

@app.get("/status")
def get_status():
    return {"status": "Server is running"}

# main block to run directly with `python server.py`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)