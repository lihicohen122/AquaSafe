from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel #To define and validate structured data (like JSON)
from typing import List #To describe a list of items with type hints

app = FastAPI()

# Allow CORS for React frontend (this is how we pass all the data to react fronend without clashing). 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#we should move this to a class in the future 
class Sensor(BaseModel):
    id: str
    bpm: int
    distance: int
    status: str  # "normal", "warning", "critical"
 
@app.get("/sensors", response_model=List[Sensor])

#just an example to check if its working 
def get_sensors():
    return [
        {"id": "Lihi", "bpm": 80, "distance": 12, "status": "normal"},
        {"id": "Noa", "bpm": 77, "distance": 14, "status": "normal"},
        {"id": "Adva", "bpm": 160, "distance": 25, "status": "critical"},
        {"id": "Adi", "bpm": 110, "distance": 20, "status": "warning"},
    ]

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
