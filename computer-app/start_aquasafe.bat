@echo off
title AquaSafe - Starting All Services
echo ====================================
echo        AquaSafe System Startup
echo ====================================
echo.

echo [1/3] Starting React Client...
start "React Client" cmd /k "cd /d %~dp0diver-distress-client && npm start"

echo [2/3] Starting Python Server...
start "Python Server" cmd /k "cd /d %~dp0server && python server.py"

echo [3/3] Starting Acoustic Server...
start "Acoustic Server" cmd /k "cd /d %~dp0Server && python acoustic_server.py"

echo.
echo ====================================
echo   All services are starting...
echo   Check the separate windows!
echo ====================================
pause
