@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"
title Push Saathi AI 2.0 to GitHub — Engineered by Pratham Prasad

set "REMOTE=https://github.com/PrathamPrasad148/SaathiAI.git"
set "COMMIT_MESSAGE=%~1"
if not defined COMMIT_MESSAGE (
    for /f "tokens=1-4 delims=/.- " %%a in ("%DATE%") do set "D_STR=%%a-%%b-%%c"
    for /f "tokens=1-3 delims=:. " %%a in ("%TIME%") do set "T_STR=%%a:%%b:%%c"
    set "COMMIT_MESSAGE=Update Saathi AI 2.0 by Pratham Prasad [!D_STR! !T_STR!]"
)

echo.
echo ========================================================
echo     Saathi AI 2.0 — GitHub Publisher (Pratham Prasad)
echo ========================================================
echo Remote: %REMOTE%
echo Commit: !COMMIT_MESSAGE!
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

:: 3. Configure Git author identity
echo [INFO] Configuring Git credentials for Pratham Prasad...
git config user.name "Pratham Prasad"
git config user.email "prathamprasad148@users.noreply.github.com"

:: 4. Ensure main branch
git branch -M main >nul 2>&1

:: 5. Setup remote origin
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo [INFO] Setting remote origin...
    git remote add origin "%REMOTE%"
) else (
    git remote set-url origin "%REMOTE%"
)

:: 6. Clean stale lock files if present
if exist ".git\index.lock" del /f /q ".git\index.lock" >nul 2>&1
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock" >nul 2>&1
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock" >nul 2>&1

:: 7. Check for 0-byte or corrupted Git index and auto-repair
if exist ".git\index" (
    for %%F in (.git\index) do (
        if %%~zF EQU 0 (
            echo [WARN] 0-byte corrupted Git index detected. Auto-repairing...
            del /f /q ".git\index" >nul 2>&1
            git reset HEAD >nul 2>&1
        )
    )
)

git status >nul 2>&1
if errorlevel 1 (
    echo [WARN] Git index error detected. Reconstructing index...
    del /f /q ".git\index" >nul 2>&1
    del /f /q ".git\index.lock" >nul 2>&1
    git reset HEAD >nul 2>&1
)

:: 8. Stage all modified and untracked files across all subdirectories
echo [INFO] Staging all files across Saathi AI 2.0 repository...
git add -A
if errorlevel 1 (
    echo [WARN] Staging encountered index lock. Retrying with fresh index...
    del /f /q ".git\index" >nul 2>&1
    git reset HEAD >nul 2>&1
    git add -A
    if errorlevel 1 goto FAILED
)

:: 9. Check if any changes need to be committed
set "HAS_CHANGES="
for /f "tokens=*" %%i in ('git status --porcelain') do (
    set "HAS_CHANGES=1"
)

if defined HAS_CHANGES (
    echo [INFO] Creating commit: !COMMIT_MESSAGE!
    git commit -m "!COMMIT_MESSAGE!"
    if errorlevel 1 (
        echo [WARN] Commit returned non-zero. Continuing to sync...
    )
) else (
    echo [INFO] Working tree is clean. Nothing to commit locally.
)

:: 10. Push to GitHub with automatic conflict resolution
echo [INFO] Pushing everything to GitHub...
git push -u origin main
if not errorlevel 1 goto SUCCESS

echo [INFO] Remote branch has new commits. Pulling with auto-sync...
git pull origin main --rebase --autostash
if errorlevel 1 (
    echo [WARN] Rebase hit a conflict. Resolving in favor of local changes...
    git rebase --abort >nul 2>&1
    git pull origin main --no-rebase -X ours --no-edit
)

echo [INFO] Retrying push to GitHub...
git push -u origin main
if errorlevel 1 goto FAILED

:SUCCESS
echo.
echo ========================================================
echo [SUCCESS] Saathi AI 2.0 successfully pushed to GitHub!
echo Author: Pratham Prasad
echo URL: %REMOTE%
echo ========================================================
exit /b 0

:FAILED
echo.
echo ========================================================
echo [FAILED] Push could not complete. Check your internet
echo connection and GitHub repository permissions.
echo ========================================================
exit /b 1
