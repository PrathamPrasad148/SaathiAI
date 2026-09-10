@echo off
SETLOCAL EnableDelayedExpansion
TITLE Saathi AI 2.0 Master Control Console — Engineered by Pratham Prasad
cd /d "%~dp0"

:: Detect Python interpreter (prefer Python 3.12)
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

:MENU
cls
echo ===================================================================
echo               SAATHI AI 2.0 — MASTER CONTROL CONSOLE
echo                    Engineered by Pratham Prasad
echo ===================================================================
echo  Repository : https://github.com/PrathamPrasad148/SaathiAI.git
echo  Platform   : Windows 10/11 64-bit | Local-First Sovereign AI
echo  Subsystems : WebCmd | SelfEdify | Acontext | ClawCode | Ponytail
echo               DeepSeekHarness | PrevJarvis | 60FPS Arc Visualizer
echo ===================================================================
echo.
echo  [1] Launch Saathi AI 2.0 HUD & Cognitive Interface
echo  [2] Run System Doctor Diagnostics (py -3.12 -m saathi doctor)
echo  [3] Run Modular Unit Test Suite (26/26 Verification)
echo  [4] Launch Continuous 24/7 Self-Advancement Daemon
echo  [5] Launch Autonomous Dev-Loop Engine (Overnight Self-Dev)
echo  [6] Push Repository to GitHub (Auto-Repair & Sync)
echo  [7] Build Android APK Package Configurations
echo  [8] Verify & Install Python Dependencies
echo  [9] Run System Integrity & Module Compilation Check
echo  [10] Exit Console
echo.
echo ===================================================================
set /p CHOICE="Select directive [1-10]: "

if "%CHOICE%"=="1" goto LAUNCH_APP
if "%CHOICE%"=="2" goto DOCTOR
if "%CHOICE%"=="3" goto RUN_TESTS
if "%CHOICE%"=="4" goto LAUNCH_ADVANCEMENT
if "%CHOICE%"=="5" goto LAUNCH_DEVLOOP
if "%CHOICE%"=="6" goto PUSH_GITHUB
if "%CHOICE%"=="7" goto BUILD_APK
if "%CHOICE%"=="8" goto INSTALL_DEPS
if "%CHOICE%"=="9" goto COMPILE_CHECK
if "%CHOICE%"=="10" goto QUIT
goto MENU

:LAUNCH_APP
cls
echo ===================================================================
echo Initializing Saathi AI 2.0 60FPS Visualizer & HUD Engine...
echo ===================================================================
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
goto MENU

:DOCTOR
cls
echo ===================================================================
echo Executing Saathi AI 2.0 System Doctor Diagnostics...
echo ===================================================================
%PY_CMD% -m saathi doctor
pause
goto MENU

:RUN_TESTS
cls
echo ===================================================================
echo Running Saathi AI 2.0 Modular Unit Test Suite...
echo ===================================================================
%PY_CMD% -m unittest discover -s tests -p "test_*.py"
pause
goto MENU

:LAUNCH_ADVANCEMENT
cls
call "%~dp0Start-Continuous-Advancement.bat"
goto MENU

:LAUNCH_DEVLOOP
cls
call "%~dp0Start-DevLoop.bat"
goto MENU

:PUSH_GITHUB
cls
call "%~dp0push-to-github.bat"
pause
goto MENU

:BUILD_APK
cls
call "%~dp0Build-Saathi-APK.bat"
goto MENU

:INSTALL_DEPS
cls
echo ===================================================================
echo Installing & Verifying Dependencies...
echo ===================================================================
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
%PY_CMD% -m compileall main.py saathi ui agent automations memory voice tools devloop
if errorlevel 1 (
    echo.
    echo [WARN] Compilation reported warnings or errors. Review output above.
) else (
    echo.
    echo [SUCCESS] All Saathi AI 2.0 modules compiled with 0 syntax errors!
)
pause
goto MENU

:QUIT
exit /b 0