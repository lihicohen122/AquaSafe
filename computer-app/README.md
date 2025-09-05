# AquaSafe - Underwater Diving Communication System

## Quick Start for Presentations
Double-click on: `start_aquasafe.bat`

This will open 3 windows:
- React Client (http://localhost:3000)
- Python Server (http://localhost:5000)
- Acoustic Server (receives underwater acoustic signals)

## Manual Startup (for Developers)

### 1. Starting the Client (React)
```bash
start_client.bat
```
or manually:
```bash
cd diver-distress-client
npm start
```

### 2. Starting the Main Server
```bash
start_server.bat
```
or manually:
```bash
cd server
python server.py
```

### 3. Starting the Acoustic Server
```bash
start_acoustic.bat
```
or manually:
```bash
cd Server
python acoustic_server.py
```

## Audio Device Configuration
On different computers, you may need to change the `input_device_index` in `Server/acoustic_server.py`: Run the server and check the available device list

## Stop All Services
Double-click on: `stop_aquasafe.bat`

## Requirements
- Node.js (for React client)
- Python with required packages (pyaudio, numpy, scipy)
- Underwater microphone connected to computer

## Project Structure
```
├── diver-distress-client/    # React frontend application
├── Server/                   # Python backend servers
│   ├── server.py            # Main FastAPI server
│   ├── acoustic_server.py   # Acoustic communication server
│   └── ...
├── start_aquasafe.bat       # Master startup script
├── start_client.bat         # Client startup script
├── start_server.bat         # Server startup script
├── start_acoustic.bat       # Acoustic server startup script
└── stop_aquasafe.bat        # Stop all services script
```

## Technology Stack
- **Frontend**: React.js
- **Backend**: Python FastAPI
- **Acoustic Communication**: Python with pyaudio
- **Database**: SQLite
- **Audio Processing**: numpy, scipy
