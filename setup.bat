@echo off
TITLE Saathi AI 2.0 - Environment Setup
echo =================================================================
echo                   SAATHI AI 2.0 INITIALIZATION                   
echo =================================================================
echo Checking Python environment...

py -3.12 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python 3.12 is required but not found. Please install Python 3.12.
    pause
    exit /b 1
)

echo Installing dependencies from requirements.txt...
py -3.12 -m pip install -r requirements.txt --quiet

echo Running Saathi System Doctor...
py -3.12 -m saathi doctor

echo =================================================================
echo            SAATHI AI 2.0 SETUP COMPLETED SUCCESSFULLY!           
echo =================================================================
pause

