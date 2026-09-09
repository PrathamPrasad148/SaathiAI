@echo off
setlocal
cd /d "%~dp0"
title Saathi AI - Continuous 24/7 Self-Advancement Daemon

echo ===================================================================
echo       SAATHI AI — CONTINUOUS 24/7 SELF-ADVANCEMENT DAEMON
echo            Web AI Browser Trainer & Multi-Agent Engine
echo ===================================================================
echo.
echo [INFO] Web AI Browser Sessions: ENABLED (Chrome / Edge User Profile)
echo [INFO] Rate Limit Auto-Switching: ACTIVE
echo [INFO] Multi-AI Consensus Synthesis: ACTIVE
echo [INFO] Dynamic Sub-Agent Scaffolding: ACTIVE
echo.

"C:\Users\prasa\AppData\Local\Programs\Python\Python312\python.exe" devloop\continuous_advancement.py %*

if errorlevel 1 (
    echo.
    echo [ERROR] Continuous Advancement Daemon exited with error code %ERRORLEVEL%.
    pause
)
exit /b 0

