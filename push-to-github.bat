@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"
title Push SaathiAI to GitHub

set "REMOTE=https://github.com/PrathamPrasad148/SaathiAI.git"
set "COMMIT_MESSAGE=%~1"
if "%COMMIT_MESSAGE%"=="" set "COMMIT_MESSAGE=Update SaathiAI (%DATE% %TIME%)"

echo.
echo ========================================================
echo               Saathi AI - GitHub Publisher
echo ========================================================
echo Remote: %REMOTE%
echo.

:: 1. Check Git availability
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git is not installed or not in system PATH.
    goto FAILED
)

:: 2. Initialize repo if needed
if not exist ".git" (
    echo [INFO] Initializing Git repository...
    git init
    if errorlevel 1 goto FAILED
)

:: 3. Ensure Git identity is set
git config user.name >nul 2>&1
if errorlevel 1 (
    echo [INFO] Configuring default Git username...
    git config user.name "PrathamPrasad148"
)
git config user.email >nul 2>&1
if errorlevel 1 (
    echo [INFO] Configuring default Git email...
    git config user.email "prathamprasad148@users.noreply.github.com"
)

:: 4. Ensure main branch
git branch -M main
if errorlevel 1 goto FAILED

:: 5. Setup remote origin
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo [INFO] Setting remote origin...
    git remote add origin "%REMOTE%"
) else (
    git remote set-url origin "%REMOTE%"
)
if errorlevel 1 goto FAILED

:: 6. Stage ALL files (code, skills, data, projects, configs)
echo [INFO] Staging all files across the repository...
git add -A
if errorlevel 1 goto FAILED

:: 7. Commit changes if any exist
git diff --cached --quiet
if errorlevel 1 (
    echo [INFO] Creating commit: %COMMIT_MESSAGE%
    git commit -m "%COMMIT_MESSAGE%"
    if errorlevel 1 goto FAILED
) else (
    echo [INFO] Everything is already up to date locally.
)

:: 8. Push to GitHub
echo [INFO] Pushing everything to GitHub...
git push -u origin main
if errorlevel 1 (
    echo [INFO] Remote branch has new commits. Pulling with auto-sync...
    git pull origin main --rebase --autostash
    if errorlevel 1 (
        echo [WARN] Rebase hit a conflict. Resolving in favor of local changes...
        git rebase --abort >nul 2>&1
        git pull origin main --no-rebase -X ours --no-edit
    )
    echo [INFO] Retrying push to GitHub...
    git push -u origin main
)
if errorlevel 1 goto FAILED

echo.
echo ========================================================
echo [SUCCESS] Everything has been pushed to GitHub!
echo URL: %REMOTE%
echo ========================================================
goto DONE

:FAILED
echo.
echo ========================================================
echo [FAILED] Push could not complete. Check your internet
echo connection and GitHub repository permissions.
echo ========================================================

:DONE
pause
exit /b 0

