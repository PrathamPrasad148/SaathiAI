@echo off
setlocal
cd /d "%~dp0"
title Saathi AI 2.0 — Environment Setup & Initialization

echo =================================================================
echo             SAATHI AI 2.0 INITIALIZATION & SETUP
echo                   Engineered by Pratham Prasad
echo =================================================================
echo.

:: 1. Detect Python 3.12
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

:: 2. Ensure data directories exist
echo [INFO] Initializing system directory structure...
if not exist "data" mkdir data
if not exist "data\logs" mkdir data\logs
if not exist "backups" mkdir backups
if not exist "Projects" mkdir Projects
if not exist "dist" mkdir dist

:: 3. Install core dependencies
echo [INFO] Installing dependencies from requirements.txt...
%PY_CMD% -m pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [WARN] Dependency installation encountered warnings/errors. Retrying verbose...
    %PY_CMD% -m pip install -r requirements.txt
)

:: 4. Run System Doctor Diagnostics
echo.
echo [INFO] Executing Saathi AI 2.0 System Doctor Diagnostics...
%PY_CMD% -m saathi doctor

:: 5. Run Unit Test Suite Verification
echo.
echo [INFO] Verifying modular architecture unit tests...
%PY_CMD% -m unittest discover -s tests -p "test_*.py"

echo.
echo =================================================================
echo         SAATHI AI 2.0 SETUP COMPLETED SUCCESSFULLY!           
echo =================================================================
pause
exit /b 0
