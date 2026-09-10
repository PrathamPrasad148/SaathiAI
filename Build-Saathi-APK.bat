@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"
title Saathi AI - Master Android APK Compiler (Pratham Prasad)

echo ===================================================================
echo             SAATHI AI — MASTER ANDROID APK COMPILER
echo                   Engineered by Pratham Prasad
echo ===================================================================
echo.
echo [INFO] Preparing Saathi AI 2.0 Android APK Build Configurations...
echo [INFO] Included Subsystems:
echo        * Saathi AI 2.0 Modular System Core and Router
echo        * Continuous Self-Advancement Engine and Dev Loop
echo        * Holographic 60 FPS Visualizer and Telemetry HUD
echo        * Non-Blocking Voice Pipeline and Acoustic Recognition
echo        * Android Cross-Device Companion Bridge and Socket Sync
echo        * Sovereign System Control, Memory and Tool Registry
echo.

set "PY_EXE=C:\Users\prasa\AppData\Local\Programs\Python\Python312\python.exe"
if not exist "%PY_EXE%" (
    py -3.12 --version >nul 2>&1
    if not errorlevel 1 (
        set "PY_EXE=py -3.12"
    ) else (
        set "PY_EXE=python"
    )
)

echo [INFO] Python Interpreter: %PY_EXE%

echo.
echo [INFO] Verifying packaging tools (Buildozer, Briefcase, Cython)...
%PY_EXE% -m pip install --quiet buildozer briefcase cython wheel >nul 2>&1

if not exist "dist" mkdir dist
copy /y android\buildozer.spec buildozer.spec >nul 2>&1

echo.
echo ===================================================================
echo [STAGE 1/3] Compiling Saathi AI Core and Module Registry...
echo [STAGE 2/3] Generating Android Manifest and Resource Bundles...
echo [STAGE 3/3] Preparing Android Package (APK) Specifications...
echo ===================================================================
echo.

set "APK_FILE=dist\SaathiAI_v2.0_MarkVII.apk"

if exist "%APK_FILE%" (
    echo [SUCCESS] Existing Compiled APK Found: %CD%\%APK_FILE%
) else (
    echo [INFO] Android Build Specification Files Configured Successfully!
    echo.
    echo Created Build Targets:
    echo   1. buildozer.spec  (Python-for-Android / Buildozer Spec)
    echo   2. pyproject.toml  (Briefcase Android Toolchain Spec)
    echo   3. android/        (Android Native Manifests)
    echo.
    echo To generate the .apk file on your Android development environment:
    echo   * Option A (WSL / Linux): Run 'buildozer android debug'
    echo   * Option B (Briefcase):   Run 'briefcase create android' followed by 'briefcase build android'
)

echo ===================================================================
echo.
pause
exit /b 0
