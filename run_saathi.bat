@echo off
setlocal
cd /d "%~dp0"
title Saathi AI 2.0 Quick Launcher

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
            set "PY_CMD=python"
        )
    )
)

echo Starting Saathi AI 2.0 Desktop Interface...
%PY_CMD% -m saathi gui %*
if errorlevel 1 (
    %PY_CMD% main.py %*
)
