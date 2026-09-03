@echo off
cd /d "%~dp0"
title Saathi AI
py -3.12 --version >nul 2>&1
if not errorlevel 1 (
    py -3.12 main.py %*
) else (
    python main.py %*
)
if errorlevel 1 pause
