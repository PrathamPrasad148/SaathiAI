@echo off
setlocal
cd /d "%~dp0"
title Saathi AI 2.0 — Autonomous Dev-Loop (Overnight Self-Development)

echo ===================================================================
echo         SAATHI AI 2.0 — AUTONOMOUS DEV-LOOP ENGINE
echo                Engineered by Pratham Prasad
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
echo [INFO] Environment: Sandboxed Git Dev Loop
echo [INFO] Live OS GUI Control: DISABLED
echo [INFO] Test Suite Verification: MANDATORY (26/26 Tests Required)
echo.

%PY_CMD% devloop\dev_loop.py %*

if errorlevel 1 (
    echo.
    echo [ERROR] Saathi Dev-Loop exited with error code %ERRORLEVEL%.
    pause
) else (
    echo.
    echo [SUCCESS] Saathi Dev-Loop finished cleanly! Review devloop_report.md for morning briefing.
)
exit /b 0
