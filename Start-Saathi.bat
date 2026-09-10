@echo off
setlocal
cd /d "%~dp0"
title Saathi AI 2.0 — Cognitive Operating Interface (Engineered by Pratham Prasad)

echo ===================================================================
echo             SAATHI AI 2.0 — COGNITIVE OPERATING INTERFACE
echo                   Engineered by Pratham Prasad
echo ===================================================================
echo.

:: 1. Dynamic Python Interpreter Detection
set "PY_CMD="
py -3.12 --version >nul 2>&1
if not errorlevel 1 (
    set "PY_CMD=py -3.12"
) else (
    python --version >nul 2>&1
    if not errorlevel 1 (
        set "PY_CMD=python"
    ) else (
        if exist "C:\Users\prasa\AppData\Local\Programs\Python\Python312\python.exe" (
            set "PY_CMD=C:\Users\prasa\AppData\Local\Programs\Python\Python312\python.exe"
        ) else (
            echo [ERROR] Python 3.12 is required but not found in PATH or standard location.
            pause
            exit /b 1
        )
    )
)

echo [INFO] Python Interpreter: %PY_CMD%

:: 2. Check and verify core dependencies
echo [INFO] Verifying system dependencies...
%PY_CMD% -c "import sounddevice, requests" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Missing dependencies detected. Installing from requirements.txt...
    %PY_CMD% -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies. Check internet connection.
        pause
        exit /b 1
    )
    echo [INFO] Dependencies installed successfully!
) else (
    echo [INFO] All core dependencies verified.
)

:: 3. Check Ollama local service status
echo [INFO] Checking local Ollama AI engine status...
curl -s http://127.0.0.1:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo [WARN] Ollama engine not detected at http://127.0.0.1:11434.
    echo [WARN] Run 'ollama serve' in a separate terminal for local AI capabilities.
) else (
    echo [INFO] Local Ollama AI engine online and active!
)

:: 4. Launch Saathi AI 2.0 HUD & Interface
echo.
echo [INFO] Launching Saathi AI 2.0 60FPS Arc Reactor Visualizer...
%PY_CMD% -m saathi gui %*
if errorlevel 1 (
    echo [INFO] Falling back to main.py launch...
    %PY_CMD% main.py %*
)

if errorlevel 1 (
    echo.
    echo [ERROR] Saathi AI exited with code %ERRORLEVEL%.
    pause
)
exit /b 0
