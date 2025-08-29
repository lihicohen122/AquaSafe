from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi import BackgroundTasks
import smtplib
from email.mime.text import MIMEText

from managers.sensor_manager import SensorManager
from models.sensor import Sensor
from routes.diver_routes import router as diver_router
from routes.group_routes import router as group_router
from routes.contact_routes import router as contact_router
from database import Base, engine

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes for sensors (not yet migrated to database, work in progress)
sensor_manager = SensorManager(None)

@app.get("/sensors", response_model=list[Sensor])
def get_sensors():
    return sensor_manager.get_all_sensors()

@app.get("/")
def read_root():
    return {"message": "Hello from Diver Distress System!"}

@app.get("/status")
def get_status():
    return {"status": "Server is running"}

# Connect divers and groups routes
app.include_router(diver_router, prefix="/divers")
app.include_router(group_router, prefix="/groups")
app.include_router(contact_router)

# main block
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
