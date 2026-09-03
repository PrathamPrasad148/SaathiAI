@echo off
setlocal
cd /d "%~dp0"
title Saathi AI

:: 1. Detect Python interpreter (prefer Python 3.12)
py -3.12 --version >nul 2>&1
if not errorlevel 1 (
    set "PY_CMD=py -3.12"
) else (
    set "PY_CMD=python"
)

echo =======================================================
echo                   SAATHI AI LAUNCHER
echo =======================================================
echo [INFO] Using interpreter: %PY_CMD%

:: 2. Check if all required packages are installed
%PY_CMD% -c "import sounddevice, faster_whisper, numpy, edge_tts, pygame, send2trash, pystray, PIL" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Missing dependencies detected.
    echo [INFO] Installing required packages from requirements.txt...
    %PY_CMD% -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies. Please check your internet connection or Python setup.
        pause
        exit /b 1
    )
    echo [INFO] All packages successfully installed!
) else (
    echo [INFO] All dependencies verified.
)

:: 3. Launch Saathi AI
echo [INFO] Launching Saathi AI...
%PY_CMD% main.py %*
if errorlevel 1 (
    echo [ERROR] Saathi AI exited with an error.
    pause
)
