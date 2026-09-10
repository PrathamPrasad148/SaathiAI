@echo off
setlocal
cd /d "%~dp0"
title Saathi AI 2.0 — Continuous 24/7 Self-Advancement Daemon

echo ===================================================================
echo     SAATHI AI 2.0 — CONTINUOUS 24/7 SELF-ADVANCEMENT DAEMON
echo            Web AI Browser Trainer & Multi-Agent Engine
echo                   Engineered by Pratham Prasad
echo ===================================================================
echo.

:: Detect Python interpreter
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
            echo [ERROR] Python 3.12 is required but not found.
            pause
            exit /b 1
        )
    )
)

echo [INFO] Python Interpreter: %PY_CMD%
echo [INFO] Web AI Browser Sessions: ENABLED (Chrome / Edge User Profile)
echo [INFO] Rate Limit Auto-Switching: ACTIVE
echo [INFO] Multi-AI Consensus Synthesis: ACTIVE
echo [INFO] Dynamic Sub-Agent Scaffolding: ACTIVE
echo.

%PY_CMD% devloop\continuous_advancement.py %*

if errorlevel 1 (
    echo.
    echo [ERROR] Continuous Advancement Daemon exited with error code %ERRORLEVEL%.
    pause
)
exit /b 0
