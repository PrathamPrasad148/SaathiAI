@echo off
setlocal
cd /d "%~dp0"
title Erase SaathiAI GitHub Repository Files

set "REMOTE=https://github.com/PrathamPrasad148/SaathiAI.git"

echo.
echo WARNING: This removes all tracked files from the GitHub main branch.
echo Local files will remain on this computer.
echo Git commit history will remain available on GitHub.
echo.
echo Repository: %REMOTE%
echo.
set /p "CONFIRM=Type ERASE to continue: "
if /I not "%CONFIRM%"=="ERASE" (
    echo.
    echo Cancelled. Nothing was changed.
    pause
    exit /b 0
)

git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git is not installed or is not available on PATH.
    goto FAILED
)

if not exist ".git" (
    echo [ERROR] This folder is not a Git repository.
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

git commit -m "Clear repository files"
if errorlevel 1 (
    echo [INFO] No tracked files remained to remove.
) else (
    git push origin main
    if errorlevel 1 goto FAILED
)

echo.
echo [SUCCESS] All tracked files were removed from the GitHub main branch.
echo Local files were left intact.
pause
exit /b 0

:FAILED
echo.
echo [FAILED] Nothing was pushed. Review the error above.
pause
exit /b 1
