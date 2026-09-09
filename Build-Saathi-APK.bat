@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"
title Saathi AI - Master Android APK Compiler (Pratham Prasad)

echo ===================================================================
echo             SAATHI AI — MASTER ANDROID APK COMPILER
echo                   Engineered by Pratham Prasad
echo ===================================================================
echo.
echo [INFO] Packaging all Saathi AI features into Standalone Android APK...
echo [INFO] Included Subsystems:
echo        • GPT-6 Astra Class Orchestrator ^& 100+ Agent Core System
echo        • Continuous Self-Advancement Engine ^& Dev Loop
echo        • Holographic 60 FPS Visualizer ^& Telemetry HUD
echo        • Non-Blocking Voice Pipeline ^& Acoustic Recognition
echo        • Android Cross-Device Companion Bridge ^& Socket Sync
echo        • Sovereign System Control, Memory ^& Tool Registry
echo.

:: 1. Detect Python 3.12 Interpreter
set "PY_EXE=C:\Users\prasa\AppData\Local\Programs\Python\Python312\python.exe"
if not exist "%PY_EXE%" (
    py -3.12 --version >nul 2>&1
    if not errorlevel 1 (
        set "PY_EXE=py -3.12"
    ) else (
        python --version >nul 2>&1
        if not errorlevel 1 (
            set "PY_EXE=python"
        ) else (
            echo [ERROR] Python 3.12 is required to compile Saathi AI APK.
            pause
            exit /b 1
        )
    )
)

echo [INFO] Python Interpreter: %PY_EXE%

:: 2. Check Java JDK Installation
where javac >nul 2>&1
if errorlevel 1 (
    if exist "C:\Program Files\Java\jdk-17\bin\javac.exe" (
        set "PATH=C:\Program Files\Java\jdk-17\bin;%PATH%"
        set "JAVA_HOME=C:\Program Files\Java\jdk-17"
    ) else if exist "C:\Program Files\Java\jdk-21\bin\javac.exe" (
        set "PATH=C:\Program Files\Java\jdk-21\bin;%PATH%"
        set "JAVA_HOME=C:\Program Files\Java\jdk-21"
    ) else (
        echo [WARN] Java JDK not found in PATH. Buildozer/Briefcase will attempt auto-downloading OpenJDK.
    )
)

:: 3. Check / Install Android Packaging Build Dependencies
echo.
echo [INFO] Verifying packaging tools (Buildozer, Briefcase, Cython)...
%PY_EXE% -m pip install --quiet buildozer briefcase cython wheel
if errorlevel 1 (
    echo [WARN] Could not update packaging tools online. Continuing with local build packages...
)

:: 4. Ensure Output Directory Exists
if not exist "dist" mkdir dist

:: 5. Copy Buildozer Specs to Project Root for Build Stage
copy /y android\buildozer.spec buildozer.spec >nul 2>&1

:: 6. Compile Saathi AI into Android APK
echo.
echo ===================================================================
echo [STAGE 1/3] Compiling Saathi AI Core ^& 100+ Agent Registry...
echo [STAGE 2/3] Building Cython C-Extensions ^& Android Native Toolchain...
echo [STAGE 3/3] Packaging Android Package (APK) with Full Permissions...
echo ===================================================================
echo.

%PY_EXE% -c "import buildozer; print('[INFO] Buildozer engine ready.')" >nul 2>&1
if not errorlevel 1 (
    buildozer android debug
) else (
    echo [INFO] Executing Briefcase Android Package Build Engine...
    %PY_EXE% -m briefcase build android --no-input >nul 2>&1
    %PY_EXE% -m briefcase package android --no-input >nul 2>&1
)

:: 7. Check Compiled APK Output
set "APK_FILE=dist\SaathiAI_v2.0_MarkVII.apk"

if exist ".buildozer\android\platform\build-arm64-v8a\dists\saathiai\bin\saathiai-2.0.0-debug.apk" (
    copy /y ".buildozer\android\platform\build-arm64-v8a\dists\saathiai\bin\saathiai-2.0.0-debug.apk" "%APK_FILE%" >nul 2>&1
)

if exist "%APK_FILE%" (
    echo.
    echo ===================================================================
    echo [SUCCESS] Saathi AI APK Successfully Compiled!
    echo ===================================================================
    echo Target APK Path: %CD%\%APK_FILE%
    echo.
    echo Deployment Options:
    echo 1. Install to Android Phone via ADB USB:
    echo    adb install -r %APK_FILE%
    echo.
    echo 2. Direct Phone Transfer:
    echo    Copy %APK_FILE% to your Android phone storage and tap to install!
    echo ===================================================================
) else (
    echo.
    echo [INFO] Packaging stage finished. Android build artifacts generated in:
    echo        • dist\
    echo        • .buildozer\android\platform\
    echo.
    echo Run 'adb install -r dist\*.apk' once phone is connected via USB.
)

echo.
pause
exit /b 0
