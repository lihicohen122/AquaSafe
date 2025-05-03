from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from managers.sensor_manager import SensorManager
from models.sensor import Sensor
from routes.diver_routes import router as diver_router
from routes.group_routes import router as group_router
from database import Base, engine

# יצירת הטבלאות במסד הנתונים אם הן לא קיימות
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

# Routes for sensors (עדיין לא הועברו למסד, עובדים על זה)
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

# מחברים את הנתיבים של divers ו-groups
app.include_router(diver_router, prefix="/divers")
app.include_router(group_router, prefix="/groups")

# main block
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
