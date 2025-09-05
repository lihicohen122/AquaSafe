@echo off
title Acoustic Server
REM Navigate to script directory
cd /d "%~dp0"
echo Starting Acoustic Server...
REM Navigate to Server folder and run acoustic server
cd Server
python acoustic_server.py
