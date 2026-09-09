@echo off
setlocal
cd /d "%~dp0"
title Saathi AI - Autonomous Dev-Loop (Overnight Self-Development)

echo ===================================================================
echo           SAATHI AI — AUTONOMOUS DEV-LOOP ENGINE
echo                 Engineered by Pratham Prasad
echo ===================================================================
echo.
echo [INFO] Environment: Sandboxed Git Dev Loop
echo [INFO] Live OS GUI Control: DISABLED
echo [INFO] Test Suite Verification: MANDATORY
echo.

"C:\Users\prasa\AppData\Local\Programs\Python\Python312\python.exe" devloop\dev_loop.py %*

if errorlevel 1 (
    echo.
    echo [ERROR] Saathi Dev-Loop exited with error code %ERRORLEVEL%.
    pause
) else (
    echo.
    echo [SUCCESS] Saathi Dev-Loop finished cleanly! Review devloop_report.md for morning briefing.
)
exit /b 0

