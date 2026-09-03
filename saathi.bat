@echo off
SETLOCAL EnableDelayedExpansion
TITLE Saathi AI Manager
cd /d "%~dp0"

:MENU
cls
echo =======================================================
echo                   SAATHI AI MANAGER
echo =======================================================
echo [1] Start Saathi AI
echo [2] Update and Push to GitHub (PrathamPrasad148/SaathiAI)
echo [3] Exit
echo =======================================================
set /p CHOICE="Select an option (1-3): "

if "%CHOICE%"=="1" goto START_SAATHI
if "%CHOICE%"=="2" goto UPDATE_GITHUB
if "%CHOICE%"=="3" goto QUIT
goto MENU

:START_SAATHI
cls
echo =======================================================
echo Starting Saathi AI...
echo =======================================================

:: 1. Check Python installation
py -3.12 --version >nul 2>&1
if not errorlevel 1 (
    set "PY_CMD=py -3.12"
) else (
    set "PY_CMD=python"
)

:: 2. Manage virtual environment if needed
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

:: 3. Run application
if exist "main.py" (
    echo [INFO] Launching main.py with %PY_CMD%...
    %PY_CMD% main.py %*
) else if exist "AI\main.py" (
    echo [INFO] Launching AI\main.py with %PY_CMD%...
    %PY_CMD% AI\main.py %*
) else (
    echo [ERROR] main.py could not be found.
)
pause
goto MENU

:UPDATE_GITHUB
cls
echo =======================================================
echo Updating GitHub: PrathamPrasad148/SaathiAI
echo =======================================================

:: 1. Check Git installation
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git is not installed or not configured in your PATH.
    pause
    goto MENU
)

:: 2. Ensure repository initialization
if not exist ".git" (
    echo [INFO] Initializing git repository...
    git init
    git branch -M main
)

:: 3. Configure origin remote
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo [INFO] Adding remote origin...
    git remote add origin https://github.com/PrathamPrasad148/SaathiAI.git
) else (
    git remote set-url origin https://github.com/PrathamPrasad148/SaathiAI.git
)

:: 4. Stage changes
echo [INFO] Staging project files...
git add .

:: 5. Commit changes
git status --porcelain | findstr /R "." >nul
if errorlevel 1 (
    echo [INFO] No local changes found to commit.
) else (
    set /p MSG="Enter commit message (Leave blank for default): "
    if "!MSG!"=="" set "MSG=Update Saathi AI configurations and scripts"
    git commit -m "!MSG!"
)

:: 6. Push to GitHub main branch
echo [INFO] Pushing changes to GitHub main...
git push -u origin main

echo.
echo [SUCCESS] Saathi AI successfully synced to GitHub!
pause
goto MENU

:QUIT
exit /b 0