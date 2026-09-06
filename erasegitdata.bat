@echo off
setlocal
cd /d "%~dp0"
title Clean Remote GitHub Repository - Pratham Prasad

set "REMOTE=https://github.com/PrathamPrasad148/SaathiAI.git"

echo ===================================================================
echo               SAATHI AI — REMOTE REPOSITORY PURGE UTILITY
echo                       Author: Pratham Prasad
echo ===================================================================
echo.
echo WARNING: This operation removes all tracked files from the GitHub
echo main branch while leaving local disk files completely intact.
echo.
echo Target Remote: %REMOTE%
echo.
set /p "CONFIRM=Type ERASE to confirm remote purge: "
if /I not "%CONFIRM%"=="ERASE" (
    echo.
    echo [INFO] Operation cancelled. No remote changes made.
    pause
    exit /b 0
)

git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git is not installed or not in PATH.
    goto FAILED
)

if not exist ".git" (
    echo [ERROR] Current folder is not a Git repository.
    goto FAILED
)

git remote set-url origin "%REMOTE%"
if errorlevel 1 goto FAILED

git fetch origin main
if errorlevel 1 goto FAILED

git checkout main
if errorlevel 1 goto FAILED

git pull --ff-only origin main
if errorlevel 1 goto FAILED

git rm -r --cached --ignore-unmatch .
if errorlevel 1 goto FAILED

git commit -m "Clear remote repository files by Pratham Prasad"
if errorlevel 1 (
    echo [INFO] No tracked files remained to clear.
) else (
    git push origin main
    if errorlevel 1 goto FAILED
)

echo.
echo ===================================================================
echo [SUCCESS] Remote tracked files purged from GitHub.
echo Local workspace files remain fully preserved on disk.
echo ===================================================================
pause
exit /b 0

:FAILED
echo.
echo [FAILED] Remote purge could not complete. Review errors above.
pause
exit /b 1
