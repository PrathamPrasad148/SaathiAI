@echo off
SETLOCAL EnableDelayedExpansion
TITLE Saathi AI Control Console - Pratham Prasad
cd /d "%~dp0"

:MENU
cls
echo ===================================================================
echo               SAATHI AI — SYSTEM MANAGEMENT CONSOLE
echo                    Engineered by Pratham Prasad
echo ===================================================================
echo  Repository : https://github.com/PrathamPrasad148/SaathiAI.git
echo  Platform   : Windows 10/11 64-bit
echo ===================================================================
echo.
echo  [1] Launch Saathi AI (Full Vector HUD & Cognitive Agent)
echo  [2] Push Repository to GitHub (Auto-Repair & Sync)
echo  [3] Verify & Install Python Dependencies
echo  [4] Run Integrity Check & Module Compilation
echo  [5] Exit Console
echo.
echo ===================================================================
set /p CHOICE="Select directive [1-5]: "

if "%CHOICE%"=="1" goto LAUNCH_APP
if "%CHOICE%"=="2" goto PUSH_GITHUB
if "%CHOICE%"=="3" goto INSTALL_DEPS
if "%CHOICE%"=="4" goto COMPILE_CHECK
if "%CHOICE%"=="5" goto QUIT
goto MENU

:LAUNCH_APP
cls
echo ===================================================================
echo Initializing Saathi AI HUD...
echo ===================================================================
py -3.12 --version >nul 2>&1
if not errorlevel 1 (
    set "PY_CMD=py -3.12"
) else (
    set "PY_CMD=python"
)

echo [INFO] Using interpreter: %PY_CMD%
%PY_CMD% main.py %*
if errorlevel 1 (
    echo.
    echo [ERROR] Saathi AI exited with code %ERRORLEVEL%.
    pause
)
goto MENU

:PUSH_GITHUB
cls
call "%~dp0push-to-github.bat"
pause
goto MENU

:INSTALL_DEPS
cls
echo ===================================================================
echo Installing & Verifying Dependencies...
echo ===================================================================
py -3.12 --version >nul 2>&1
if not errorlevel 1 (
    set "PY_CMD=py -3.12"
) else (
    set "PY_CMD=python"
)
%PY_CMD% -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Dependency installation encountered an issue.
) else (
    echo [SUCCESS] All requirements satisfied!
)
pause
goto MENU

:COMPILE_CHECK
cls
echo ===================================================================
echo Running System Integrity & Bytecode Compilation...
echo ===================================================================
py -3.12 --version >nul 2>&1
if not errorlevel 1 (
    set "PY_CMD=py -3.12"
) else (
    set "PY_CMD=python"
)
%PY_CMD% -m compileall main.py ui agent automations memory voice tools
if errorlevel 1 (
    echo.
    echo [WARN] Compilation reported warnings or errors. Review output above.
) else (
    echo.
    echo [SUCCESS] All modules compiled with 0 syntax errors!
)
pause
goto MENU

:QUIT
exit /b 0