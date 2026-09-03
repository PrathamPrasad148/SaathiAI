@echo off
setlocal
cd /d "%~dp0"
title Push SaathiAI to GitHub

set "REMOTE=https://github.com/PrathamPrasad148/SaathiAI.git"
set "COMMIT_MESSAGE=%~1"
if "%COMMIT_MESSAGE%"=="" set "COMMIT_MESSAGE=Update SaathiAI"

echo.
echo SaathiAI GitHub publisher
echo ========================

git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git is not installed or is not available on PATH.
    goto FAILED
)

if not exist ".git" (
    echo [INFO] Initializing the local Git repository...
    git init
    if errorlevel 1 goto FAILED
)

git branch -M main
if errorlevel 1 goto FAILED

git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo [INFO] Adding GitHub remote...
    git remote add origin "%REMOTE%"
) else (
    echo [INFO] Updating GitHub remote...
    git remote set-url origin "%REMOTE%"
)
if errorlevel 1 goto FAILED

echo [INFO] Staging project files...
git add -A
if errorlevel 1 goto FAILED

git diff --cached --quiet
if errorlevel 1 (
    echo [INFO] Creating commit: %COMMIT_MESSAGE%
    git commit -m "%COMMIT_MESSAGE%"
    if errorlevel 1 goto FAILED
) else (
    echo [INFO] No new local changes to commit.
)

echo [INFO] Pushing all committed project files to GitHub...
git push -u origin main
if errorlevel 1 (
    echo [INFO] Pulling remote updates with rebase...
    git pull --rebase origin main
    git push -u origin main
)
if errorlevel 1 goto FAILED

echo.
echo [SUCCESS] SaathiAI was pushed to:
echo %REMOTE%
goto DONE

:FAILED
echo.
echo [FAILED] Nothing was pushed. Review the error above.

:DONE
pause
exit /b 0
