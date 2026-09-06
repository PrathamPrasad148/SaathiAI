@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

set "REMOTE=https://github.com/PrathamPrasad148/SaathiAI.git"
set "COMMIT_MESSAGE=%~1"
if not defined COMMIT_MESSAGE (
    for /f "tokens=1-4 delims=/.- " %%a in ("%DATE%") do set "D_STR=%%a-%%b-%%c"
    for /f "tokens=1-3 delims=:. " %%a in ("%TIME%") do set "T_STR=%%a:%%b:%%c"
    set "COMMIT_MESSAGE=Update Saathi AI by Pratham Prasad [!D_STR! !T_STR!]"
)

echo Commit message: "!COMMIT_MESSAGE!"

:: 1. Auto clean locks
if exist ".git\index.lock" del /f /q ".git\index.lock" >nul 2>&1
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock" >nul 2>&1
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock" >nul 2>&1

:: 2. Fix 0-byte corrupted index
if exist ".git\index" (
    for %%F in (.git\index) do (
        if %%~zF EQU 0 (
            echo [WARN] 0-byte Git index detected. Rebuilding...
            del /f /q ".git\index" >nul 2>&1
            git reset HEAD >nul 2>&1
        )
    )
)

:: 3. Stage
git add -A

:: 4. Check if anything needs committing
set "HAS_CHANGES="
for /f "tokens=*" %%i in ('git status --porcelain') do (
    set "HAS_CHANGES=1"
)

if defined HAS_CHANGES (
    echo [INFO] Committing changes...
    git commit -m "!COMMIT_MESSAGE!"
) else (
    echo [INFO] Working tree clean. Nothing to commit.
)

:: 5. Push
echo [INFO] Pushing to origin main...
git push -u origin main
if not errorlevel 1 goto SUCCESS

echo [INFO] Syncing with remote...
git pull origin main --rebase --autostash
if errorlevel 1 (
    git rebase --abort >nul 2>&1
    git pull origin main --no-rebase -X ours --no-edit
)
git push -u origin main
if errorlevel 1 goto FAILED

:SUCCESS
echo [SUCCESS] Push completed successfully!
exit /b 0

:FAILED
echo [FAILED] Push failed.
exit /b 1
