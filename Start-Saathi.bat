@echo off
setlocal
cd /d "%~dp0"
title Saathi AI - Cognitive Operating Interface (Pratham Prasad)

echo ===================================================================
echo             SAATHI AI — COGNITIVE OPERATING INTERFACE
echo                   Engineered by Pratham Prasad
echo ===================================================================
echo.

:: 1. Detect Python interpreter (prefer Python 3.12)
py -3.12 --version >nul 2>&1
if not errorlevel 1 (
    set "PY_CMD=py -3.12"
) else (
    python --version >nul 2>&1
    if not errorlevel 1 (
        set "PY_CMD=python"
    ) else (
        echo [ERROR] Python is not found. Please install Python 3.12.
        pause
        exit /b 1
    )
)

echo [INFO] Python Interpreter: %PY_CMD%

:: 2. Check and verify required packages
echo [INFO] Checking system dependencies...
%PY_CMD% -c "import sounddevice, faster_whisper, numpy, edge_tts, pygame, send2trash, pystray, PIL" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Missing dependencies detected. Installing from requirements.txt...
    %PY_CMD% -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies. Check internet connection.
        pause
        exit /b 1
    )
    echo [INFO] All packages successfully installed!
) else (
    echo [INFO] All core dependencies verified.
)

:: 3. Check Ollama service availability
echo [INFO] Checking local Ollama engine status...
curl -s http://127.0.0.1:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo [WARN] Ollama does not seem to be running at http://127.0.0.1:11434.
    echo [WARN] Start Ollama in another terminal with 'ollama serve' for local AI features.
) else (
    echo [INFO] Ollama engine detected and online!
)

:: 4. Launch Saathi AI
echo.
echo [INFO] Initializing Saathi AI HUD...
%PY_CMD% main.py %*
if errorlevel 1 (
    echo.
    echo [ERROR] Saathi AI exited with code %ERRORLEVEL%.
    pause
)
exit /b 0
