# AquaSafe

AquaSafe is a real-time diver monitoring system, consisting of three main components:
- **Python Server (FastAPI):** Handles data management, receives acoustic data from the watch, and provides an API for the management app.
- **Watch App (Android/Kotlin):** Collects heart rate data from a smartwatch and transmits it acoustically to the server.
- **Desktop App (React):** Management interface for viewing diver status, groups, and alerts.

---

## Project Structure

```
computer-app/
  Server/                # Server code (FastAPI, SQLAlchemy)
  diver-distress-client/ # React app (management interface)
watch-app/               # Android watch app
```

---

## Installation & Running

### 1. Server (FastAPI)

**Prerequisites:**  
- Python 3.9+
- Install dependencies:  
  ```sh
  pip install fastapi uvicorn sqlalchemy pydantic
  ```

**Run:**
```sh
cd computer-app/Server
uvicorn server:app --reload --host 0.0.0.0 --port 5000
```
The API will be available at `http://localhost:5000`.

### 2. Desktop App (React)

**Prerequisites:**  
- Node.js 18+

**Run:**
```sh
cd computer-app/diver-distress-client
npm install
npm start
```
The app will open at `http://localhost:3000`.

### 3. Watch App (Android)

**Prerequisites:**  
- Android Studio
- Smartwatch with heart rate sensor (Wear OS)

**Run:**
1. Open the `watch-app` folder in Android Studio.
2. Connect your watch/emulator.
3. Click Run.

---

## Component Overview

### Server
- Written in Python with FastAPI.
- Stores diver and group data in SQLite.
- Receives acoustic data from the watch (`acoustic_server.py`).
- Provides a REST API for the management app.

### Desktop App (React)
- Management interface for viewing divers, groups, and alerts.
- Communicates with the server via API.
- Code located in [computer-app/diver-distress-client](computer-app/diver-distress-client).

### Watch App (Android)
- Collects heart rate from the sensor.
- Transmits data acoustically (using sound frequencies) to the server.
- Code located in [watch-app/app/src/main/java/com/example/diversensorapp/MainActivity.kt](watch-app/app/src/main/java/com/example/diversensorapp/MainActivity.kt).

---

## Basic Flow Diagram

1. **Watch** measures heart rate, transmits acoustically to the server.
2. **Server** receives, decodes, and stores the data.
3. **Desktop app** displays diver status and alerts in real time.

---

## Contributing

- Pull requests are welcome!
- Please refer to each component's folder for specific code.

---

## Authors

- AquaSafe Team

---

## License

MIT License / Apache 2.0 (depending on components)